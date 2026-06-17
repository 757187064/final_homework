"""RLE 编码与解码工具。

Kaggle Severstal 的 Mask 使用 Run-Length Encoding 保存：
- 像素位置从 1 开始计数；
- 展开顺序是列优先，也就是 Fortran order；
- 空缺陷通常表示为空字符串或缺失值。
"""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def is_empty_rle(rle: object) -> bool:
    """判断一条 RLE 是否表示空 Mask。"""
    if rle is None:
        return True
    if isinstance(rle, float) and math.isnan(rle):
        return True
    if isinstance(rle, str) and not rle.strip():
        return True
    return False


def rle_decode(rle: object, shape: tuple[int, int] = (256, 1600)) -> np.ndarray:
    """将 Kaggle RLE 字符串解码为二维二值 Mask。

    Args:
        rle: 形如 ``"1 3 10 5"`` 的字符串，表示从第 1 个像素开始连续 3 个、
            从第 10 个像素开始连续 5 个。空值会返回全 0 Mask。
        shape: ``(height, width)``。

    Returns:
        ``uint8`` 数组，形状为 ``(height, width)``，缺陷像素为 1。
    """
    height, width = shape
    mask = np.zeros(height * width, dtype=np.uint8)
    if is_empty_rle(rle):
        return mask.reshape((height, width), order="F")

    values = [int(x) for x in str(rle).split()]
    starts = np.asarray(values[0::2], dtype=np.int64) - 1
    lengths = np.asarray(values[1::2], dtype=np.int64)
    ends = starts + lengths

    for start, end in zip(starts, ends):
        mask[start:end] = 1

    return mask.reshape((height, width), order="F")


def rle_encode(mask: np.ndarray) -> str:
    """将二维二值 Mask 编码为 Kaggle RLE 字符串。

    Args:
        mask: 形状为 ``(height, width)`` 的数组，非 0 像素视为缺陷。

    Returns:
        RLE 字符串；如果 Mask 为空，返回空字符串。
    """
    if mask.ndim != 2:
        raise ValueError(f"rle_encode 只接受二维 Mask，当前维度为 {mask.ndim}")

    pixels = (mask > 0).astype(np.uint8).flatten(order="F")
    padded = np.concatenate([[0], pixels, [0]])
    changes = np.where(padded[1:] != padded[:-1])[0] + 1
    runs = changes.copy()
    runs[1::2] -= runs[0::2]
    return " ".join(str(x) for x in runs)


def stack_rles(
    rles: Iterable[object],
    shape: tuple[int, int] = (256, 1600),
) -> np.ndarray:
    """把 4 个类别的 RLE 组合成多通道 Mask，输出 ``(H, W, C)``。"""
    masks = [rle_decode(rle, shape=shape) for rle in rles]
    return np.stack(masks, axis=-1).astype(np.float32)

