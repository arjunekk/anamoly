"""
PatchCore anomaly detector.

Combines the feature extractor, patch aggregation, and memory bank into
a single class with two operations: fit() to build the memory bank from
training data, and predict() to score a new image at inference time.
"""

import torch
from pathlib import Path

from app.feature_extraction.extractor import WideResNetFeatureExtractor
from app.anomaly_detection.patch_aggregator import aggregate_patch_features
from app.anomaly_detection.memory_bank import MemoryBank


class PatchCore:
    def __init__(self, subsample_ratio: float = 0.1):
        self.extractor = WideResNetFeatureExtractor()
        self.memory_bank = MemoryBank(subsample_ratio=subsample_ratio)

    def fit(self, dataloader):
        """
        Builds the memory bank from a DataLoader of training ('good') images.
        """
        all_patches = []

        for batch in dataloader:
            feat2, feat3 = self.extractor(batch)
            patch_features = aggregate_patch_features(feat2, feat3)  # [B, 784, 1536]

            # Flatten batch and patch dimensions into one long list of vectors.
            batch_size, num_patches, channels = patch_features.shape
            flattened = patch_features.reshape(batch_size * num_patches, channels)
            all_patches.append(flattened)

        all_patches = torch.cat(all_patches, dim=0)
        self.memory_bank.build(all_patches)

    def predict(self, image_batch: torch.Tensor):
        """
        Args:
            image_batch: shape [1, 3, 224, 224] — a single preprocessed image.

        Returns:
            image_score: a single float, the overall anomaly score.
            heatmap: shape [28, 28], per-patch anomaly scores.
        """
        feat2, feat3 = self.extractor(image_batch)
        patch_features = aggregate_patch_features(feat2, feat3)  # [1, 784, 1536]

        patch_features = patch_features.squeeze(0)  # [784, 1536]
        distances = self.memory_bank.query(patch_features)  # [784]

        # Reshape flat per-patch distances back into a 28x28 spatial heatmap.
        heatmap = distances.reshape(28, 28)

        # Image-level score: the single most anomalous patch drives the
        # overall score, since even one badly abnormal region should flag
        # the whole product as defective.
        image_score = distances.max().item()

        return image_score, heatmap

    def save(self, path: str):
        self.memory_bank.save(path)

    def load(self, path: str):
        self.memory_bank.load(path)