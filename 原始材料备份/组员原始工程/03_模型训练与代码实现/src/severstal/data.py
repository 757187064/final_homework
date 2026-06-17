"""数据读取、标注整理与 Dataset。

Severstal 的 ``train.csv`` 包含 ``ImageId``、``ClassId``、``EncodedPixels`` 三列，
其中 ClassId 取值 1~4 对应四种缺陷类型。
本模块会把它整理成"一张图片一行、4 个类别各一列"的格式，便于训练多通道分割模型。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from severstal.rle import is_empty_rle


CLASS_COLUMNS = [f"class_{i}" for i in range(1, 5)]


def prepare_train_dataframe(csv_path: str | Path) -> pd.DataFrame:
    """把原始 train.csv 聚合成训练用 DataFrame。

    原始 train.csv 包含三列：
    - ``ImageId``：图片文件名；
    - ``ClassId``：缺陷类别（1~4）；
    - ``EncodedPixels``：RLE 编码的掩码。

    返回列：
    - ``image_id``：图片文件名；
    - ``class_1`` ~ ``class_4``：每类缺陷对应的 RLE；
    - ``has_defect``：是否至少有一个类别存在缺陷。
    """
    raw = pd.read_csv(csv_path)

    # 确保实际列名大小写兼容
    columns_lower = [col.lower() for col in raw.columns]
    if "imageid" not in columns_lower and "classid" not in columns_lower:
        if "image_id" in columns_lower and "class_id" in columns_lower:
            pass  # 兼容下划线命名
        else:
            raise ValueError(
                "train.csv 必须包含 ImageId、ClassId、EncodedPixels 三列（列名不区分大小写）。"
            )
    if "encodedpixels" not in columns_lower:
        raise ValueError("train.csv 必须包含 EncodedPixels 列。")

    # 统一列名为小写进行后续操作
    rename_map = {}
    for col in raw.columns:
        lower = col.lower()
        if lower in ("imageid", "image_id"):
            rename_map[col] = "image_id"
        elif lower in ("classid", "class_id"):
            rename_map[col] = "class_id"
        elif lower == "encodedpixels":
            rename_map[col] = "EncodedPixels"
    raw = raw.rename(columns=rename_map)

    # 确保 class_id 为整数
    raw["class_id"] = raw["class_id"].astype(int)

    table = raw.pivot(index="image_id", columns="class_id", values="EncodedPixels")
    table = table.rename(columns={i: f"class_{i}" for i in range(1, 5)})
    for column in CLASS_COLUMNS:
        if column not in table.columns:
            table[column] = np.nan
    table = table[CLASS_COLUMNS].reset_index()
    # Kaggle 原始空标注通常会被 pandas 读成 NaN；这里也兼容空字符串。
    defect_flags = table[CLASS_COLUMNS].apply(
        lambda column: column.map(lambda x: not is_empty_rle(x))
    )
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
    """从 sample_submission.csv 提取测试图片列表。

    sample_submission.csv 使用 ``ImageId_ClassId`` 合并列（Kaggle 标准格式），
    例如 ``a.jpg_1``。本函数从中提取不重复的图片文件名。
    """
    sample = pd.read_csv(sample_submission_path)

    # 判断是 ImageId_ClassId 合并列还是 ImageId/ClassId 分开
    columns_lower = [col.lower() for col in sample.columns]
    if "imageid" in columns_lower:
        # 三列分开格式：直接用 ImageId 列
        image_col = [col for col in sample.columns if col.lower() == "imageid"][0]
        image_ids = sorted(sample[image_col].unique())
    elif "imageid_classid" in columns_lower or "image_id" in columns_lower:
        # Kaggle 标准合并列：ImageId_ClassId，从中提取 ImageId 部分
        id_col = [col for col in sample.columns if col.lower() in ("imageid_classid", "image_id")][0]
        image_ids = sorted({str(v).rsplit("_", 1)[0] for v in sample[id_col]})
    else:
        raise ValueError(
            "sample_submission.csv 必须包含 ImageId_ClassId 列，或 ImageId + ClassId 两列"
        )
    return pd.DataFrame({"image_id": image_ids})
