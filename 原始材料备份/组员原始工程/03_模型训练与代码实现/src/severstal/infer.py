"""推理与提交文件生成。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from severstal.config import load_config
from severstal.data import prepare_test_dataframe
from severstal.dataset import SeverstalDataset
from severstal.models import create_model
from severstal.rle import rle_encode
from severstal.transforms import get_valid_transforms
from severstal.utils import get_device, resolve_data_path


def resize_mask_to_raw(mask: np.ndarray, raw_size: tuple[int, int]) -> np.ndarray:
    """把模型输出 Mask 恢复到原始提交尺寸。"""
    if mask.shape == raw_size:
        return mask
    import cv2

    raw_height, raw_width = raw_size
    return cv2.resize(mask, (raw_width, raw_height), interpolation=cv2.INTER_NEAREST)


@torch.no_grad()
def predict_masks(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    threshold: float,
) -> dict[str, np.ndarray]:
    """对测试集预测 4 通道二值 Mask。"""
    model.eval()
    predictions: dict[str, np.ndarray] = {}

    for batch in tqdm(loader, desc="infer"):
        images = batch["image"].to(device)
        logits = model(images)
        probs = torch.sigmoid(logits).detach().cpu().numpy()
        masks = (probs > threshold).astype(np.uint8)

        for image_id, mask in zip(batch["image_id"], masks):
            predictions[image_id] = mask.transpose(1, 2, 0)

    return predictions


def create_submission(
    config: dict[str, Any],
    checkpoint_path: str | Path,
    output_path: str | Path,
) -> Path:
    """加载模型并生成 Kaggle submission.csv。"""
    data_cfg = config["data"]
    sample_path = resolve_data_path(data_cfg["root"], data_cfg["sample_submission"])
    if sample_path is None:
        raise ValueError("配置文件 data.sample_submission 不能为空，推理需要 sample_submission.csv")
    test_image_dir = resolve_data_path(data_cfg["root"], data_cfg["test_images"])
    test_df = prepare_test_dataframe(sample_path)

    image_size = (int(data_cfg["image_height"]), int(data_cfg["image_width"]))
    mask_size = (
        int(data_cfg.get("raw_height", data_cfg["image_height"])),
        int(data_cfg.get("raw_width", data_cfg["image_width"])),
    )
    dataset = SeverstalDataset(
        test_df,
        image_dir=test_image_dir,
        image_size=image_size,
        mask_size=mask_size,
        transforms=get_valid_transforms(image_size=image_size),
        return_mask=False,
    )
    loader = DataLoader(
        dataset,
        batch_size=int(config["train"]["batch_size"]),
        shuffle=False,
        num_workers=int(data_cfg.get("num_workers", 0)),
        pin_memory=torch.cuda.is_available(),
    )

    device = get_device()
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model_config = checkpoint.get("config", config)["model"]
    # 推理时不需要下载预训练权重，后续 load_state_dict 会覆盖
    model_config["encoder_weights"] = None
    model = create_model(model_config).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])

    predictions = predict_masks(
        model,
        loader,
        device,
        threshold=float(config["train"]["threshold"]),
    )

    sample = pd.read_csv(sample_path)

    # 判断 sample_submission 格式：ImageId_ClassId 合并列，还是 ImageId + ClassId 分开
    columns_lower = [col.lower() for col in sample.columns]
    if "imageid_classid" in columns_lower or "image_id" in columns_lower:
        # Kaggle 标准合并列格式
        id_col = [col for col in sample.columns if col.lower() in ("imageid_classid", "image_id")][0]
        combined_fmt = True
    else:
        combined_fmt = False

    encoded_pixels: list[str] = []
    for _, row in sample.iterrows():
        if combined_fmt:
            # 从 ImageId_ClassId 解析出 image_id 和 class_id
            image_class = str(row[id_col])
            image_id, class_id_text = image_class.rsplit("_", 1)
            class_index = int(class_id_text) - 1
        else:
            image_id = str(row["ImageId"])
            class_index = int(row["ClassId"]) - 1
        mask = predictions[image_id][..., class_index]
        mask = resize_mask_to_raw(mask, raw_size=mask_size)
        encoded_pixels.append(rle_encode(mask))

    if combined_fmt:
        # 已经是 ImageId_ClassId 格式，直接更新 EncodedPixels 即可
        sample["EncodedPixels"] = encoded_pixels
    else:
        # 合并 ImageId 和 ClassId 为 Kaggle 要求的 ImageId_ClassId 格式
        sample["ImageId_ClassId"] = sample["ImageId"].astype(str) + "_" + sample["ClassId"].astype(str)
        sample["EncodedPixels"] = encoded_pixels
        sample = sample[["ImageId_ClassId", "EncodedPixels"]]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(output_path, index=False)
    print(f"提交文件已保存：{output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 Severstal 提交文件")
    parser.add_argument("--config", required=True, help="YAML 配置文件路径")
    parser.add_argument("--checkpoint", required=True, help="训练得到的 best_model.pth")
    parser.add_argument("--output", required=True, help="submission.csv 输出路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    create_submission(config, args.checkpoint, args.output)


if __name__ == "__main__":
    main()
