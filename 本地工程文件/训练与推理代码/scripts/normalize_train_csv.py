"""把 train.csv 统一转换为 Kaggle 标准格式。

标准格式：
- ImageId_ClassId
- EncodedPixels

如果输入已经是标准格式，会原样整理输出；如果输入是 ImageId、ClassId、
EncodedPixels 三列，会合并成 ImageId_ClassId。
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def normalize_train_csv(input_path: str | Path, output_path: str | Path) -> None:
    """转换 train.csv 为 ImageId_ClassId + EncodedPixels 格式。"""
    input_path = Path(input_path)
    output_path = Path(output_path)
    dataframe = pd.read_csv(input_path)

    if {"ImageId_ClassId", "EncodedPixels"}.issubset(dataframe.columns):
        normalized = dataframe[["ImageId_ClassId", "EncodedPixels"]].copy()
    elif {"ImageId", "ClassId", "EncodedPixels"}.issubset(dataframe.columns):
        normalized = pd.DataFrame(
            {
                "ImageId_ClassId": dataframe["ImageId"].astype(str)
                + "_"
                + dataframe["ClassId"].astype(str),
                "EncodedPixels": dataframe["EncodedPixels"],
            }
        )
    else:
        raise ValueError(
            "输入 train.csv 必须包含 ImageId_ClassId + EncodedPixels，"
            "或 ImageId + ClassId + EncodedPixels"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(output_path, index=False)
    print(f"已保存标准格式 train.csv：{output_path}")
    print(f"行数：{len(normalized)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统一 train.csv 标注格式")
    parser.add_argument("--input", required=True, help="原始 train.csv 路径")
    parser.add_argument("--output", required=True, help="标准格式 train.csv 输出路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    normalize_train_csv(args.input, args.output)


if __name__ == "__main__":
    main()
