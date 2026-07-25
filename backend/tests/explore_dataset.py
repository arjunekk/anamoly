"""
Dataset exploration script.

Purpose: Verify the MVTec AD 'bottle' category is correctly downloaded
and understand its structure BEFORE writing any loader or model code.

This is a one-off diagnostic script, not part of the production pipeline —
it lives in tests/ rather than app/ for that reason.
"""

import os
from pathlib import Path

DATASET_ROOT = Path("dataset/mvtec_ad/bottle")


def count_images(folder: Path) -> int:
    """Count image files in a folder, ignoring non-image files."""
    if not folder.exists():
        return 0
    valid_extensions = {".png", ".jpg", ".jpeg"}
    return sum(1 for f in folder.iterdir() if f.suffix.lower() in valid_extensions)


def explore_split(split_name: str, split_path: Path):
    """Print image counts for each subfolder in a train/test split."""
    print(f"\n{split_name.upper()} SPLIT: {split_path}")
    if not split_path.exists():
        print("  ⚠️  Folder not found.")
        return

    for subfolder in sorted(split_path.iterdir()):
        if subfolder.is_dir():
            count = count_images(subfolder)
            print(f"  {subfolder.name:20s} -> {count} images")


def main():
    print("=" * 50)
    print("MVTec AD - Bottle Category - Dataset Exploration")
    print("=" * 50)

    if not DATASET_ROOT.exists():
        print(f"❌ Dataset not found at: {DATASET_ROOT.resolve()}")
        print("Make sure you've downloaded and extracted the bottle category.")
        return

    explore_split("train", DATASET_ROOT / "train")
    explore_split("test", DATASET_ROOT / "test")
    explore_split("ground_truth", DATASET_ROOT / "ground_truth")

    print("\n" + "=" * 50)
    print("Exploration complete.")


if __name__ == "__main__":
    main()