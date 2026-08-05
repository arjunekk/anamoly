"""
Tests for MVTecGoodImageDataset (Phase 3).
"""

import torch
from app.preprocessing.dataset_loader import MVTecGoodImageDataset


def test_dataset_loads_expected_number_of_images(category_root):
    dataset = MVTecGoodImageDataset(category_root)
    assert len(dataset) == 209


def test_sample_tensor_has_correct_shape(category_root):
    dataset = MVTecGoodImageDataset(category_root)
    sample = dataset[0]
    assert sample.shape == torch.Size([3, 224, 224])


def test_sample_tensor_is_normalized(category_root):
    """
    Confirms ImageNet normalization was actually applied — raw pixels
    range 0-1, normalized values should extend outside that range.
    """
    dataset = MVTecGoodImageDataset(category_root)
    sample = dataset[0]
    assert sample.min() < 0 or sample.max() > 1