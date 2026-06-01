"""模型构建模块。"""

from __future__ import annotations

from typing import Any


def create_model(config: dict[str, Any]):
    """创建语义分割模型。

    当前默认使用 segmentation_models_pytorch 的 U-Net。后续做消融时，
    只需要修改配置里的 encoder 或 architecture。
    """
    import segmentation_models_pytorch as smp

    architecture = config.get("architecture", "unet").lower()
    common_kwargs = {
        "encoder_name": config.get("encoder_name", "resnet34"),
        "encoder_weights": config.get("encoder_weights", None),
        "in_channels": int(config.get("in_channels", 3)),
        "classes": int(config.get("classes", 4)),
    }

    if architecture == "unet":
        return smp.Unet(**common_kwargs)
    if architecture == "fpn":
        return smp.FPN(**common_kwargs)
    if architecture == "deeplabv3plus":
        return smp.DeepLabV3Plus(**common_kwargs)

    raise ValueError(f"暂不支持的模型结构：{architecture}")
