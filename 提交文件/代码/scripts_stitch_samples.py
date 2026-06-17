"""按类别拼接 3 张样本图，输出标注前（原图拼接）和标注后（Mask 叠加拼接）。"""

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import numpy as np

from src_severstal_data import prepare_train_dataframe, read_rgb_image
from src_severstal_rle import rle_decode, is_empty_rle
from src_severstal_utils import ensure_dir

CLASS_COLORS = [
    np.array([255, 0, 0], dtype=np.uint8),
    np.array([0, 180, 0], dtype=np.uint8),
    np.array([0, 90, 255], dtype=np.uint8),
    np.array([255, 180, 0], dtype=np.uint8),
]


def stitch_per_class(
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

        if len(defect_df) < samples_per_class:
            print(f"{col} 仅 {len(defect_df)} 个样本，跳过")
            continue

        color = CLASS_COLORS[class_idx - 1]

        images = []
        overlays = []
        titles = []

        for _, row in defect_df.iterrows():
            image = read_rgb_image(image_dir / row["image_id"])
            rle_str = row[col]
            mask = rle_decode(rle_str, shape=image_size)

            color_mask = np.zeros((*image_size, 3), dtype=np.uint8)
            color_mask[mask > 0] = color

            overlay = (image * 0.6 + color_mask * 0.4).astype(np.uint8)

            images.append(image)
            overlays.append(overlay)
            titles.append(row["image_id"])

        raw_stitch = np.concatenate(images, axis=0)
        overlay_stitch = np.concatenate(overlays, axis=0)

        for label, data in [("raw", raw_stitch), ("masked", overlay_stitch)]:
            fig, axis = plt.subplots(figsize=(9.6, 9))
            axis.imshow(data)
            axis.axis("off")

            if label == "masked":
                color_name = ["Red", "Green", "Blue", "Orange"][class_idx - 1]
                axis.text(
                    0.5, -0.12,
                    f"Class {class_idx} — {color_name} = defect area",
                    transform=axis.transAxes,
                    fontsize=14, fontweight="bold",
                    ha="center", va="top",
                )

            fig.tight_layout(pad=0)
            output_path = output_dir / f"class_{class_idx}_{label}_stitch.png"
            fig.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0)
            plt.close(fig)
            print(f"已保存：{output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="每类 3 样本拼接")
    parser.add_argument("--data-root", default="data/raw")
    parser.add_argument("--output-dir", default="outputs/data_analysis")
    parser.add_argument("--samples", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    stitch_per_class(
        train_csv=data_root / "train.csv",
        image_dir=data_root / "train_images",
        output_dir=args.output_dir,
        samples_per_class=args.samples,
    )


if __name__ == "__main__":
    main()

