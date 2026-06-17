"""训练脚本包装器。

这样写可以让使用者直接执行 ``python scripts/train.py``，
同时核心逻辑仍保留在 ``src/severstal`` 包中。
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from severstal.train import main


if __name__ == "__main__":
    main()
