"""评价指标。"""

from __future__ import annotations

import torch


def dice_coefficient(
    logits: torch.Tensor,
    targets: torch.Tensor,
    threshold: float = 0.5,
    eps: float = 1e-7,
) -> torch.Tensor:
    """计算 batch 级平均 Dice。

    这里先对 sigmoid 概率做阈值化，再计算 4 个类别的平均 Dice。
    """
    probs = torch.sigmoid(logits)
    preds = (probs > threshold).float()
    targets = targets.float()

    dims = (0, 2, 3)
    intersection = torch.sum(preds * targets, dims)
    denominator = torch.sum(preds + targets, dims)
    dice = (2.0 * intersection + eps) / (denominator + eps)
    return dice.mean()
