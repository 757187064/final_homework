"""训练脚本包装器。

这样写可以让使用者直接执行 ``python scripts_train.py``，
同时核心逻辑仍保留在 ``扁平源码文件 src_severstal_*.py`` 包中。
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src_severstal_train import main


if __name__ == "__main__":
    main()

