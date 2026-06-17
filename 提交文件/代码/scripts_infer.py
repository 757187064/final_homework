"""推理脚本包装器。"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src_severstal_infer import main


if __name__ == "__main__":
    main()

