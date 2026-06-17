"""数据分析与样本可视化工具。"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src_severstal_data import CLASS_COLUMNS, prepare_train_dataframe, read_rgb_image
from src_severstal_rle import is_empty_rle, stack_rles
from src_severstal_utils import ensure_dir
from src_severstal_visualize import mask_to_overlay


def summarize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """统计每类缺陷样本数和占比。"""
    total_images = len(dataframe)
    rows = []
    for index, column in enumerate(CLASS_COLUMNS, start=1):
        count = dataframe[column].map(lambda x: not is_empty_rle(x)).sum()
        rows.append(
            {
                "class_id": index,
                "defect_images": int(count),
                "ratio": float(count / total_images) if total_images else 0.0,
            }
        )
    rows.append(
        {
            "class_id": "any",
            "defect_images": int(dataframe["has_defect"].sum()),
            "ratio": float(dataframe["has_defect"].mean()) if total_images else 0.0,
        }
    )
    return pd.DataFrame(rows)


def save_class_distribution(summary: pd.DataFrame, output_path: str | Path) -> None:
    """保存类别分布柱状图。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plot_df = summary.copy()
    plot_df["class_id"] = plot_df["class_id"].astype(str)

    fig, axis = plt.subplots(figsize=(7, 4))
    axis.bar(plot_df["class_id"], plot_df["defect_images"], color="#2f6f73")
    axis.set_xlabel("Defect class")
    axis.set_ylabel("Image count")
    axis.set_title("Class Distribution")
    for i, value in enumerate(plot_df["defect_images"]):
        axis.text(i, value, str(value), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def save_sample_visualization(
    dataframe: pd.DataFrame,
    image_dir: str | Path,
    output_path: str | Path,
    max_items: int = 6,
    image_size: tuple[int, int] = (256, 1600),
) -> None:
    """保存若干有缺陷样本的图片与 Mask 叠加图。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    defect_df = dataframe[dataframe["has_defect"] == 1].head(max_items)
    if defect_df.empty:
        return

    fig, axes = plt.subplots(len(defect_df), 2, figsize=(12, 3 * len(defect_df)))
    if len(defect_df) == 1:
        axes = axes.reshape(1, 2)

    for row_index, (_, row) in enumerate(defect_df.iterrows()):
        image = read_rgb_image(Path(image_dir) / row["image_id"])
        mask = stack_rles([row[column] for column in CLASS_COLUMNS], shape=image_size)
        overlay = mask_to_overlay(mask)

        axes[row_index, 0].imshow(image)
        axes[row_index, 0].set_title(row["image_id"])
        axes[row_index, 1].imshow(image)
        axes[row_index, 1].imshow(overlay, alpha=0.45)
        axes[row_index, 1].set_title("Mask overlay")
        for axis in axes[row_index]:
            axis.axis("off")

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_data_analysis(
    train_csv: str | Path,
    image_dir: str | Path,
    output_dir: str | Path,
    image_size: tuple[int, int] = (256, 1600),
) -> None:
    """生成数据统计表、类别分布图和样本可视化图。"""
    output_dir = ensure_dir(output_dir)
    dataframe = prepare_train_dataframe(train_csv)
    summary = summarize_dataframe(dataframe)
    summary.to_csv(output_dir / "class_distribution.csv", index=False)
    save_class_distribution(summary, output_dir / "class_distribution.png")
    save_sample_visualization(
        dataframe,
        image_dir=image_dir,
        output_path=output_dir / "sample_masks.png",
        image_size=image_size,
    )
    print(f"数据分析结果已保存到：{output_dir}")

