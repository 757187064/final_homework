"""训练曲线和预测结果可视化。"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch


CLASS_COLORS = np.array(
    [
        [255, 0, 0],
        [0, 180, 0],
        [0, 90, 255],
        [255, 180, 0],
    ],
    dtype=np.uint8,
)


def mask_to_overlay(mask: np.ndarray) -> np.ndarray:
    """把 4 通道 Mask 转成彩色叠加层。"""
    overlay = np.zeros((*mask.shape[:2], 3), dtype=np.uint8)
    for class_index in range(mask.shape[-1]):
        overlay[mask[..., class_index] > 0] = CLASS_COLORS[class_index]
    return overlay


def save_prediction_grid(
    images: torch.Tensor,
    targets: torch.Tensor,
    logits: torch.Tensor,
    output_path: str | Path,
    threshold: float = 0.5,
    max_items: int = 4,
) -> None:
    """保存验证集预测对比图：原图、真实 Mask、预测 Mask。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    images_np = images.detach().cpu().numpy().transpose(0, 2, 3, 1)
    targets_np = targets.detach().cpu().numpy().transpose(0, 2, 3, 1)
    preds_np = (torch.sigmoid(logits).detach().cpu().numpy() > threshold).astype(np.uint8)
    preds_np = preds_np.transpose(0, 2, 3, 1)

    count = min(max_items, images_np.shape[0])
    fig, axes = plt.subplots(count, 3, figsize=(12, 3 * count))
    if count == 1:
        axes = np.expand_dims(axes, axis=0)

    for i in range(count):
        image = np.clip(images_np[i], 0, 1)
        target_overlay = mask_to_overlay(targets_np[i])
        pred_overlay = mask_to_overlay(preds_np[i])

        axes[i, 0].imshow(image)
        axes[i, 0].set_title("Image")
        axes[i, 1].imshow(image)
        axes[i, 1].imshow(target_overlay, alpha=0.45)
        axes[i, 1].set_title("Ground Truth")
        axes[i, 2].imshow(image)
        axes[i, 2].imshow(pred_overlay, alpha=0.45)
        axes[i, 2].set_title("Prediction")
        for axis in axes[i]:
            axis.axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def save_history_plot(history_csv: str | Path, output_path: str | Path) -> None:
    """根据 history.csv 画训练曲线。"""
    history = pd.read_csv(history_csv)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(history["epoch"], history["train_loss"], label="train")
    axes[0].plot(history["epoch"], history["val_loss"], label="val")
    axes[0].set_title("Loss")
    axes[0].legend()

    axes[1].plot(history["epoch"], history["val_dice"], label="val dice")
    axes[1].set_title("Dice")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

