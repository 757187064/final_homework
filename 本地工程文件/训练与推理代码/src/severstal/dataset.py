"""PyTorch Dataset 定义。

该文件依赖 torch，和纯数据整理函数分开，方便在本地缺少 PyTorch 时仍能测试
RLE、CSV 聚合等轻量逻辑。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import Dataset

from severstal.data import CLASS_COLUMNS, read_rgb_image
from severstal.rle import stack_rles


class SeverstalDataset(Dataset):
    """Severstal 训练/验证/测试 Dataset。"""

    def __init__(
        self,
        dataframe,
        image_dir: str | Path,
        image_size: tuple[int, int] = (256, 1600),
        mask_size: tuple[int, int] = (256, 1600),
        transforms: Any | None = None,
        return_mask: bool = True,
    ) -> None:
        self.dataframe = dataframe.reset_index(drop=True)
        self.image_dir = Path(image_dir)
        self.image_size = image_size
        self.mask_size = mask_size
        self.transforms = transforms
        self.return_mask = return_mask

    def __len__(self) -> int:
        return len(self.dataframe)

    def __getitem__(self, index: int) -> dict[str, Any]:
        row = self.dataframe.iloc[index]
        image_id = row["image_id"]
        image = read_rgb_image(self.image_dir / image_id)

        if self.return_mask:
            rles = [row[column] for column in CLASS_COLUMNS]
            mask = stack_rles(rles, shape=self.mask_size)
        else:
            mask = np.zeros((*self.image_size, 4), dtype=np.float32)

        if self.transforms is not None:
            if self.return_mask:
                augmented = self.transforms(image=image, mask=mask)
                image = augmented["image"]
                mask = augmented["mask"]
            else:
                augmented = self.transforms(image=image)
                image = augmented["image"]

        image = image.astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image.transpose(2, 0, 1)).float()

        sample: dict[str, Any] = {
            "image": image_tensor,
            "image_id": image_id,
        }

        if self.return_mask:
            mask_tensor = torch.from_numpy(mask.transpose(2, 0, 1)).float()
            sample["mask"] = mask_tensor

        return sample
