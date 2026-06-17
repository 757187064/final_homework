"""按缺陷类别各提取一张原始钢板图（无 Mask 叠加）。"""

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt

from src_severstal_data import prepare_train_dataframe, read_rgb_image
from src_severstal_rle import is_empty_rle
from src_severstal_utils import ensure_dir


def extract_raw_images(
    train_csv: Path,
    image_dir: Path,
    output_dir: Path,
) -> None:
    output_dir = ensure_dir(output_dir)
    dataframe = prepare_train_dataframe(train_csv)

    for class_idx in range(1, 5):
        col = f"class_{class_idx}"
        has_defect = dataframe[col].map(lambda x: not is_empty_rle(x))
        defect_df = dataframe[has_defect]
        if defect_df.empty:
            print(f"{col} 没有样本，跳过")
            continue

        row = defect_df.iloc[0]
        image = read_rgb_image(image_dir / row["image_id"])

        fig, axis = plt.subplots(figsize=(16, 3))
        axis.imshow(image)
        axis.set_title(f"Class {class_idx} — {row['image_id']}", fontsize=14)
        axis.axis("off")
        fig.tight_layout(pad=0)

        output_path = output_dir / f"class_{class_idx}_raw.png"
        fig.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        print(f"已保存：{output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按类别提取原始钢板图")
    parser.add_argument("--data-root", default="data/raw")
    parser.add_argument("--output-dir", default="outputs/data_analysis")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    extract_raw_images(
        train_csv=data_root / "train.csv",
        image_dir=data_root / "train_images",
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()

