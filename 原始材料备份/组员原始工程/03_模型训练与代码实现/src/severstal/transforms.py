"""Albumentations 数据增强配置。"""

from __future__ import annotations

import albumentations as A


def get_train_transforms(
    mode: str = "light",
    image_size: tuple[int, int] = (256, 1600),
) -> A.Compose:
    """根据实验配置创建训练增强。

    ``none`` 用于消融实验；``light`` 用于 Baseline；``strong`` 用于完整方案。
    """
    height, width = image_size
    resize = A.Resize(height=height, width=width)

    if mode == "none":
        return A.Compose(
            [
                resize,
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0),
            ]
        )

    if mode == "light":
        return A.Compose(
            [
                resize,
                A.HorizontalFlip(p=0.5),
                A.ShiftScaleRotate(
                    shift_limit=0.02,
                    scale_limit=0.05,
                    rotate_limit=3,
                    border_mode=0,
                    p=0.4,
                ),
                A.RandomBrightnessContrast(p=0.3),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0),
            ]
        )

    if mode == "strong":
        return A.Compose(
            [
                resize,
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.1),
                A.ShiftScaleRotate(
                    shift_limit=0.03,
                    scale_limit=0.08,
                    rotate_limit=5,
                    border_mode=0,
                    p=0.5,
                ),
                A.OneOf(
                    [
                        A.RandomBrightnessContrast(),
                        A.CLAHE(),
                        A.HueSaturationValue(),
                    ],
                    p=0.4,
                ),
                A.GaussNoise(p=0.2),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0),
            ]
        )

    raise ValueError(f"未知的数据增强模式：{mode}")


def get_valid_transforms(image_size: tuple[int, int] = (256, 1600)) -> A.Compose:
    """验证/推理阶段不做随机增强，只 resize + ImageNet normalize。"""
    height, width = image_size
    return A.Compose(
        [
            A.Resize(height=height, width=width),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0),
        ]
    )
