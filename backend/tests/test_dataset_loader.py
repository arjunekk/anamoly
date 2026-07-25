"""
Verification script for MVTecGoodImageDataset.

Purpose: Confirm the dataset loads the correct number of images and
that each image is transformed into a tensor of the expected shape,
BEFORE this class is used inside the feature extraction pipeline (Phase 5).
"""

from pathlib import Path
from app.preprocessing.dataset_loader import MVTecGoodImageDataset

CATEGORY_ROOT = Path("dataset/mvtec_ad/bottle")


def main():
    dataset = MVTecGoodImageDataset(CATEGORY_ROOT)

    print(f"Number of training images loaded: {len(dataset)}")

    sample_tensor = dataset[0]
    print(f"Sample tensor shape: {sample_tensor.shape}")
    print(f"Sample tensor dtype: {sample_tensor.dtype}")
    print(f"Sample tensor min/max: {sample_tensor.min():.3f} / {sample_tensor.max():.3f}")


if __name__ == "__main__":
    main()