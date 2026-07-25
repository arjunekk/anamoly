"""
Verification script for the DataLoader and preprocessing reversibility.

Purpose:
1. Confirm the DataLoader correctly yields batches of the expected shape.
2. Confirm preprocessing is reversible by un-normalizing a sample and
   saving it as a viewable image, BEFORE this pipeline feeds into
   feature extraction (Phase 5).
"""

from pathlib import Path
from app.preprocessing.dataloader_factory import get_train_dataloader
from app.preprocessing.visualize import unnormalize_tensor

CATEGORY_ROOT = Path("dataset/mvtec_ad/bottle")


def main():
    dataloader = get_train_dataloader(CATEGORY_ROOT, batch_size=16)

    # Pull one batch and confirm shape
    batch = next(iter(dataloader))
    print(f"Batch shape: {batch.shape}")  # expected: [16, 3, 224, 224]

    # Take the first image in the batch and reverse preprocessing
    single_tensor = batch[0]
    restored_image = unnormalize_tensor(single_tensor)

    output_path = "backend/tests/restored_sample.png"
    restored_image.save(output_path)
    print(f"Restored image saved to {output_path}")


if __name__ == "__main__":
    main()