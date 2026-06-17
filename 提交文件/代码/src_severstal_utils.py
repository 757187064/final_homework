"""通用训练工具。"""

from __future__ import annotations

import os
import random
from pathlib import Path
from typing import Any

import numpy as np
import torch


def seed_everything(seed: int) -> None:
    """固定随机种子，减少消融实验中的随机干扰。"""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    """自动选择可用设备：优先 CUDA，其次 Apple MPS，最后 CPU。"""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def ensure_dir(path: str | Path) -> Path:
    """确保目录存在并返回 Path。"""
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output


def resolve_data_path(root: str | Path, name: str | None) -> Path | None:
    """把配置中的数据相对路径解析为实际路径。"""
    if name is None:
        return None
    path = Path(name)
    if path.is_absolute():
        return path
    return Path(root) / path


def to_python_number(value: Any) -> Any:
    """把 numpy 标量转成普通 Python 类型，便于写入 JSON/CSV。"""
    if hasattr(value, "item"):
        return value.item()
    return value

