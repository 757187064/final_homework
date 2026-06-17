import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from severstal.data import prepare_train_dataframe


def test_prepare_train_dataframe(tmp_path):
    csv_path = tmp_path / "train.csv"
    pd.DataFrame(
        {
            "ImageId_ClassId": [
                "a.jpg_1",
                "a.jpg_2",
                "a.jpg_3",
                "a.jpg_4",
                "b.jpg_1",
                "b.jpg_2",
                "b.jpg_3",
                "b.jpg_4",
            ],
            "EncodedPixels": ["1 2", None, None, None, None, "3 4", None, None],
        }
    ).to_csv(csv_path, index=False)

    dataframe = prepare_train_dataframe(csv_path)

    assert list(dataframe["image_id"]) == ["a.jpg", "b.jpg"]
    assert dataframe.loc[0, "class_1"] == "1 2"
    assert dataframe.loc[1, "class_2"] == "3 4"
    assert dataframe["has_defect"].tolist() == [1, 1]
