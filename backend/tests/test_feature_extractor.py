"""
Tests for WideResNetFeatureExtractor (Phase 5).
"""

import pytest
import torch

from app.preprocessing.dataloader_factory import get_train_dataloader
from app.feature_extraction.extractor import WideResNetFeatureExtractor


@pytest.mark.slow
def test_feature_extractor_output_shapes(category_root):
    dataloader = get_train_dataloader(category_root, batch_size=8)
    batch = next(iter(dataloader))

    extractor = WideResNetFeatureExtractor()
    feat_layer2, feat_layer3 = extractor(batch)

    assert feat_layer2.shape == torch.Size([8, 512, 28, 28])
    assert feat_layer3.shape == torch.Size([8, 1024, 14, 14])