"""按缺陷类别分别生成样本 Mask 叠加图。"""

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np

from severstal.data import CLASS_COLUMNS, prepare_train_dataframe, read_rgb_image
from severstal.rle import rle_decode, is_empty_rle
from severstal.utils import ensure_dir

CLASS_NAMES = {
    1: "Class 1", 2: "Class 2", 3: "Class 3", 4: "Class 4"
}
CLASS_COLORS = [
    np.array([255, 0, 0], dtype=np.uint8),
    np.array([0, 180, 0], dtype=np.uint8),
    np.array([0, 90, 255], dtype=np.uint8),
    np.array([255, 180, 0], dtype=np.uint8),
]


def generate_per_class_visualizations(
    train_csv: Path,
    image_dir: Path,
    output_dir: Path,
    image_size: tuple[int, int] = (256, 1600),
    samples_per_class: int = 3,
) -> None:
    output_dir = ensure_dir(output_dir)
    dataframe = prepare_train_dataframe(train_csv)

    for class_idx in range(1, 5):
        col = f"class_{class_idx}"
        has_defect = dataframe[col].map(lambda x: not is_empty_rle(x))
        defect_df = dataframe[has_defect].head(samples_per_class)

        if defect_df.empty:
            print(f"{col} 没有样本，跳过")
            continue

        fig, axes = plt.subplots(
            len(defect_df), 2,
            figsize=(12, 3 * len(defect_df)),
        )
        if len(defect_df) == 1:
            axes = np.array([axes])

        for row_idx, (_, row) in enumerate(defect_df.iterrows()):
            image = read_rgb_image(image_dir / row["image_id"])
            rle_str = row[col]
            mask = rle_decode(rle_str, shape=image_size)
            color_mask = np.zeros((*image_size, 3), dtype=np.uint8)
            color_mask[mask > 0] = CLASS_COLORS[class_idx - 1]

            axes[row_idx, 0].imshow(image)
            axes[row_idx, 0].set_title(row["image_id"], fontsize=9)
            axes[row_idx, 1].imshow(image)
            axes[row_idx, 1].imshow(color_mask, alpha=0.5)
            axes[row_idx, 1].set_title(f"Mask ({CLASS_NAMES[class_idx]})", fontsize=9)
            for axis in axes[row_idx]:
                axis.axis("off")

        fig.suptitle(
            f"Defect Class {class_idx} — Sample Masks",
            fontsize=14, fontweight="bold",
        )
        fig.tight_layout()
        output_path = output_dir / f"class_{class_idx}_samples.png"
        fig.savefig(output_path, dpi=200)
        plt.close(fig)
        print(f"已保存：{output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按缺陷类别生成样本 Mask 图")
    parser.add_argument("--data-root", default="data/raw", help="数据根目录")
    parser.add_argument("--output-dir", default="outputs/data_analysis", help="输出目录")
    parser.add_argument("--samples", type=int, default=3, help="每类展示样本数")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    generate_per_class_visualizations(
        train_csv=data_root / "train.csv",
        image_dir=data_root / "train_images",
        output_dir=args.output_dir,
        samples_per_class=args.samples,
    )


if __name__ == "__main__":
    main()
