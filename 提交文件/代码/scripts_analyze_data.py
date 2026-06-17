"""生成数据统计与样本可视化。"""

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src_severstal_analysis import run_data_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="分析 Severstal 数据集")
    parser.add_argument("--data-root", default="data/raw", help="数据根目录")
    parser.add_argument("--output-dir", default="outputs/data_analysis", help="输出目录")
    parser.add_argument("--height", type=int, default=256, help="图片高度")
    parser.add_argument("--width", type=int, default=1600, help="图片宽度")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    run_data_analysis(
        train_csv=data_root / "train.csv",
        image_dir=data_root / "train_images",
        output_dir=args.output_dir,
        image_size=(args.height, args.width),
    )


if __name__ == "__main__":
    main()

