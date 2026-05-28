"""数据读取、标注整理与 Dataset。

Severstal 的标注常见两种格式：
- Kaggle 原始/提交样例风格：``ImageId_ClassId`` + ``EncodedPixels``；
- 已拆分风格：``ImageId`` + ``ClassId`` + ``EncodedPixels``。

本模块会把它们统一整理成“一张图片一行、4 个类别各一列”的格式，
便于训练多通道分割模型。
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


def _normalize_train_columns(raw: pd.DataFrame) -> pd.DataFrame:
    """兼容两种 train.csv 格式，统一得到 image_id/class_id/EncodedPixels。"""
    if "ImageId_ClassId" in raw.columns and "EncodedPixels" in raw.columns:
        parsed = raw["ImageId_ClassId"].apply(parse_image_class_id)
        return raw.assign(
            image_id=parsed.apply(lambda x: x[0]),
            class_id=parsed.apply(lambda x: x[1]),
        )

    required = {"ImageId", "ClassId", "EncodedPixels"}
    if required.issubset(raw.columns):
        return raw.assign(
            image_id=raw["ImageId"].astype(str),
            class_id=raw["ClassId"].astype(int),
        )

    raise ValueError(
        "train.csv 必须包含 ImageId_ClassId + EncodedPixels，"
        "或 ImageId + ClassId + EncodedPixels"
    )


def _list_image_ids(image_dir: str | Path | None) -> list[str]:
    """列出图片目录中的图片文件名，用于补充无缺陷空 Mask 样本。"""
    if image_dir is None:
        return []
    image_path = Path(image_dir)
    if not image_path.exists():
        return []
    suffixes = {".jpg", ".jpeg", ".png"}
    return sorted(path.name for path in image_path.iterdir() if path.suffix.lower() in suffixes)


def prepare_train_dataframe(
    csv_path: str | Path,
    image_dir: str | Path | None = None,
    include_empty_images: bool = True,
) -> pd.DataFrame:
    """把原始 train.csv 聚合成训练用 DataFrame。

    返回列：
    - ``image_id``：图片文件名；
    - ``class_1`` ~ ``class_4``：每类缺陷对应的 RLE；
    - ``has_defect``：是否至少有一个类别存在缺陷。
    """
    raw = _normalize_train_columns(pd.read_csv(csv_path))

    table = raw.pivot(index="image_id", columns="class_id", values="EncodedPixels")
    table = table.rename(columns={i: f"class_{i}" for i in range(1, 5)})
    for column in CLASS_COLUMNS:
        if column not in table.columns:
            table[column] = np.nan
    table = table[CLASS_COLUMNS].reset_index()

    if include_empty_images:
        all_image_ids = _list_image_ids(image_dir)
        if all_image_ids:
            table = (
                pd.DataFrame({"image_id": all_image_ids})
                .merge(table, on="image_id", how="left")
            )

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
    parsed = sample["ImageId_ClassId"].apply(parse_image_class_id)
    image_ids = sorted({image_id for image_id, _ in parsed})
    return pd.DataFrame({"image_id": image_ids})
