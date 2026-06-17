import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src_severstal_rle import rle_decode, rle_encode


def test_rle_roundtrip_simple_mask():
    mask = np.zeros((4, 5), dtype=np.uint8)
    mask[0, 0] = 1
    mask[1, 0] = 1
    mask[3, 4] = 1

    encoded = rle_encode(mask)
    decoded = rle_decode(encoded, shape=mask.shape)

    assert np.array_equal(mask, decoded)


def test_empty_rle_returns_zero_mask():
    decoded = rle_decode("", shape=(3, 4))

    assert decoded.shape == (3, 4)
    assert decoded.sum() == 0

