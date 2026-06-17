"""数据读取、标注整理与 Dataset。

Severstal 的 ``train.csv`` 每一行是一个 ``ImageId_ClassId`` 和一个 RLE。
本模块会把它整理成“一张图片一行、4 个类别各一列”的格式，便于训练多通道分割模型。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from severstal.rle import is_empty_rle


CLASS_COLUMNS = [f"class_{i}" for i in range(1, 5)]


def parse_image_class_id(value: str) -> tuple[str, int]:
    """解析 Kaggle 字段 ``ImageId_ClassId``。"""
    image_id, class_id = value.rsplit("_", 1)
    return image_id, int(class_id)


def prepare_train_dataframe(csv_path: str | Path) -> pd.DataFrame:
    """把原始 train.csv 聚合成训练用 DataFrame。

    返回列：
    - ``image_id``：图片文件名；
    - ``class_1`` ~ ``class_4``：每类缺陷对应的 RLE；
    - ``has_defect``：是否至少有一个类别存在缺陷。
    """
    raw = pd.read_csv(csv_path)
    if "EncodedPixels" not in raw.columns:
        raise ValueError("train.csv 必须包含 EncodedPixels 列")

    if "ImageId" in raw.columns and "ClassId" in raw.columns:
        raw = raw.assign(image_id=raw["ImageId"], class_id=raw["ClassId"])
    elif "ImageId_ClassId" in raw.columns:
        parsed = raw["ImageId_ClassId"].apply(parse_image_class_id)
        raw = raw.assign(
            image_id=parsed.apply(lambda x: x[0]),
            class_id=parsed.apply(lambda x: x[1]),
        )
    else:
        raise ValueError("train.csv 必须包含 ImageId_ClassId 或 (ImageId 和 ClassId) 列")

    table = raw.pivot(index="image_id", columns="class_id", values="EncodedPixels")
    table = table.rename(columns={i: f"class_{i}" for i in range(1, 5)})
    for column in CLASS_COLUMNS:
        if column not in table.columns:
            table[column] = np.nan
    table = table[CLASS_COLUMNS].reset_index()
    # Kaggle 原始空标注通常会被 pandas 读成 NaN；这里也兼容空字符串。
    defect_flags = table[CLASS_COLUMNS].apply(lambda column: column.map(lambda x: not is_empty_rle(x)))
    table["has_defect"] = defect_flags.any(axis=1).astype(int)
    return table


def split_train_val(
    dataframe: pd.DataFrame,
    val_ratio: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """划分训练集和验证集，并尽量保持有缺陷/无缺陷比例一致。"""
    from sklearn.model_selection import train_test_split

    stratify = dataframe["has_defect"] if dataframe["has_defect"].nunique() > 1 else None
    train_df, val_df = train_test_split(
        dataframe,
        test_size=val_ratio,
        random_state=seed,
        shuffle=True,
        stratify=stratify,
    )
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True)


def limit_dataframe(dataframe: pd.DataFrame, max_samples: int | None) -> pd.DataFrame:
    """Debug 模式限制样本数，避免本地机器压力过大。"""
    if max_samples is None:
        return dataframe
    return dataframe.head(int(max_samples)).reset_index(drop=True)


def read_rgb_image(path: str | Path) -> np.ndarray:
    """读取 RGB 图片。OpenCV 默认 BGR，这里转成深度学习常用的 RGB。"""
    import cv2

    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"无法读取图片：{path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def prepare_test_dataframe(sample_submission_path: str | Path) -> pd.DataFrame:
    """从 sample_submission.csv 提取测试图片列表。"""
    sample = pd.read_csv(sample_submission_path)
    if "ImageId" in sample.columns:
        image_ids = sorted(sample["ImageId"].unique())
    elif "ImageId_ClassId" in sample.columns:
        parsed = sample["ImageId_ClassId"].apply(parse_image_class_id)
        image_ids = sorted({image_id for image_id, _ in parsed})
    else:
        raise ValueError("sample_submission.csv 必须包含 ImageId 或 ImageId_ClassId 列")
    return pd.DataFrame({"image_id": image_ids})
