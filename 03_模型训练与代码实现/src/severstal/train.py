"""训练入口。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from severstal.config import load_config, save_config
from severstal.data import (
    limit_dataframe,
    prepare_train_dataframe,
    split_train_val,
)
from severstal.dataset import SeverstalDataset
from severstal.losses import BCEDiceLoss
from severstal.metrics import dice_coefficient
from severstal.models import create_model
from severstal.transforms import get_train_transforms, get_valid_transforms
from severstal.utils import ensure_dir, get_device, resolve_data_path, seed_everything
from severstal.visualize import save_history_plot, save_prediction_grid


def build_loaders(config: dict[str, Any]) -> tuple[DataLoader, DataLoader]:
    """根据配置构建训练/验证 DataLoader。"""
    data_cfg = config["data"]
    train_csv = resolve_data_path(data_cfg["root"], data_cfg["train_csv"])
    train_image_dir = resolve_data_path(data_cfg["root"], data_cfg["train_images"])

    dataframe = prepare_train_dataframe(train_csv)
    train_df, val_df = split_train_val(
        dataframe,
        val_ratio=float(data_cfg["val_ratio"]),
        seed=int(config["experiment"]["seed"]),
    )
    train_df = limit_dataframe(train_df, data_cfg.get("max_train_samples"))
    val_df = limit_dataframe(val_df, data_cfg.get("max_val_samples"))

    image_size = (int(data_cfg["image_height"]), int(data_cfg["image_width"]))
    mask_size = (
        int(data_cfg.get("raw_height", data_cfg["image_height"])),
        int(data_cfg.get("raw_width", data_cfg["image_width"])),
    )
    train_dataset = SeverstalDataset(
        train_df,
        image_dir=train_image_dir,
        image_size=image_size,
        mask_size=mask_size,
        transforms=get_train_transforms(
            config["train"].get("augmentation", "light"),
            image_size=image_size,
        ),
    )
    val_dataset = SeverstalDataset(
        val_df,
        image_dir=train_image_dir,
        image_size=image_size,
        mask_size=mask_size,
        transforms=get_valid_transforms(image_size=image_size),
    )

    return (
        DataLoader(
            train_dataset,
            batch_size=int(config["train"]["batch_size"]),
            shuffle=True,
            num_workers=int(data_cfg.get("num_workers", 0)),
            pin_memory=torch.cuda.is_available(),
        ),
        DataLoader(
            val_dataset,
            batch_size=int(config["train"]["batch_size"]),
            shuffle=False,
            num_workers=int(data_cfg.get("num_workers", 0)),
            pin_memory=torch.cuda.is_available(),
        ),
    )


def train_one_epoch(
    model: torch.nn.Module,
    loader: DataLoader,
    criterion: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    use_amp: bool,
) -> float:
    """训练一个 epoch。"""
    model.train()
    total_loss = 0.0
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp and device.type == "cuda")

    for batch in tqdm(loader, desc="train", leave=False):
        images = batch["image"].to(device)
        masks = batch["mask"].to(device)

        optimizer.zero_grad(set_to_none=True)
        with torch.cuda.amp.autocast(enabled=use_amp and device.type == "cuda"):
            logits = model(images)
            loss = criterion(logits, masks)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        total_loss += loss.item() * images.size(0)

    return total_loss / len(loader.dataset)


@torch.no_grad()
def validate(
    model: torch.nn.Module,
    loader: DataLoader,
    criterion: torch.nn.Module,
    device: torch.device,
    threshold: float,
    visual_path: Path | None = None,
    visual_count: int = 4,
) -> tuple[float, float]:
    """验证一个 epoch，并可保存预测可视化。"""
    model.eval()
    total_loss = 0.0
    total_dice = 0.0
    saved_visual = False

    for batch in tqdm(loader, desc="valid", leave=False):
        images = batch["image"].to(device)
        masks = batch["mask"].to(device)
        logits = model(images)
        loss = criterion(logits, masks)
        dice = dice_coefficient(logits, masks, threshold=threshold)

        total_loss += loss.item() * images.size(0)
        total_dice += dice.item() * images.size(0)

        if visual_path is not None and not saved_visual:
            save_prediction_grid(
                images,
                masks,
                logits,
                visual_path,
                threshold=threshold,
                max_items=visual_count,
            )
            saved_visual = True

    return total_loss / len(loader.dataset), total_dice / len(loader.dataset)


def run_training(config_path: str | Path) -> Path:
    """运行完整训练流程，返回最佳模型路径。"""
    config = load_config(config_path)
    seed_everything(int(config["experiment"]["seed"]))

    output_dir = ensure_dir(config["experiment"]["output_dir"])
    save_config(config, output_dir / "config.yaml")

    train_loader, val_loader = build_loaders(config)
    device = get_device()
    print(f"使用设备：{device}")

    model = create_model(config["model"]).to(device)
    criterion = BCEDiceLoss(**config["loss"])
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(config["train"]["learning_rate"]),
        weight_decay=float(config["train"].get("weight_decay", 0.0)),
    )

    scheduler = None
    if config["train"].get("use_scheduler", True):
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=int(config["train"]["epochs"]),
        )

    history_path = output_dir / "history.csv"
    best_model_path = output_dir / "best_model.pth"
    best_dice = -1.0

    with history_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["epoch", "train_loss", "val_loss", "val_dice", "lr"],
        )
        writer.writeheader()

        for epoch in range(1, int(config["train"]["epochs"]) + 1):
            train_loss = train_one_epoch(
                model,
                train_loader,
                criterion,
                optimizer,
                device,
                use_amp=bool(config["train"].get("use_amp", True)),
            )
            visual_path = None
            if config["train"].get("save_val_visuals", True):
                visual_path = output_dir / "val_predictions" / f"epoch_{epoch:03d}.png"

            val_loss, val_dice = validate(
                model,
                val_loader,
                criterion,
                device,
                threshold=float(config["train"]["threshold"]),
                visual_path=visual_path,
                visual_count=int(config["train"].get("val_visuals_count", 4)),
            )

            if scheduler is not None:
                scheduler.step()

            lr = optimizer.param_groups[0]["lr"]
            writer.writerow(
                {
                    "epoch": epoch,
                    "train_loss": train_loss,
                    "val_loss": val_loss,
                    "val_dice": val_dice,
                    "lr": lr,
                }
            )
            f.flush()

            print(
                f"epoch={epoch} train_loss={train_loss:.4f} "
                f"val_loss={val_loss:.4f} val_dice={val_dice:.4f}"
            )

            if val_dice > best_dice:
                best_dice = val_dice
                torch.save(
                    {
                        "model_state_dict": model.state_dict(),
                        "config": config,
                        "best_dice": best_dice,
                    },
                    best_model_path,
                )

    save_history_plot(history_path, output_dir / "history.png")
    print(f"最佳模型已保存：{best_model_path}")
    return best_model_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="训练 Severstal 分割模型")
    parser.add_argument("--config", required=True, help="YAML 配置文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_training(args.config)


if __name__ == "__main__":
    main()
