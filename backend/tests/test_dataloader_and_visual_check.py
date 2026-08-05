"""
Tests for DataLoader batching and preprocessing reversibility (Phase 4).
"""

import torch
from PIL import Image

from app.preprocessing.dataloader_factory import get_train_dataloader
from app.preprocessing.visualize import unnormalize_tensor


def test_dataloader_yields_correct_batch_shape(category_root):
    dataloader = get_train_dataloader(category_root, batch_size=16)
    batch = next(iter(dataloader))
    assert batch.shape == torch.Size([16, 3, 224, 224])


def test_unnormalize_produces_valid_image(category_root):
    """
    Confirms the un-normalize step produces a valid, viewable image —
    not that it LOOKS correct (that still requires a human), but that
    it's structurally valid: right type, right pixel value range.
    """
    dataloader = get_train_dataloader(category_root, batch_size=1)
    batch = next(iter(dataloader))

    restored = unnormalize_tensor(batch[0])

    assert isinstance(restored, Image.Image)
    assert restored.size == (224, 224)

    # Every pixel value must be a valid 0-255 byte.
    import numpy as np
    pixel_array = np.array(restored)
    assert pixel_array.min() >= 0
    assert pixel_array.max() <= 255