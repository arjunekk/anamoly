"""
Verification script for WideResNetFeatureExtractor.

Purpose: Confirm the extractor loads pretrained weights correctly and
produces feature maps of the expected shape, BEFORE these features are
used to build PatchCore's memory bank (Phase 6).
"""

from pathlib import Path
from app.preprocessing.dataloader_factory import get_train_dataloader
from app.feature_extraction.extractor import WideResNetFeatureExtractor

CATEGORY_ROOT = Path("dataset/mvtec_ad/bottle")


def main():
    dataloader = get_train_dataloader(CATEGORY_ROOT, batch_size=8)
    batch = next(iter(dataloader))

    extractor = WideResNetFeatureExtractor()
    feat_layer2, feat_layer3 = extractor(batch)

    print(f"Input batch shape:   {batch.shape}")
    print(f"layer2 feature shape: {feat_layer2.shape}")
    print(f"layer3 feature shape: {feat_layer3.shape}")


if __name__ == "__main__":
    main()