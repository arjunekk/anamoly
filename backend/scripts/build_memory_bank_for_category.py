"""
Builds (or rebuilds) a PatchCore memory bank for a single specified
category, with a configurable subsample ratio.

Useful for targeted experiments — e.g. testing whether a richer memory
bank (higher subsample_ratio) improves performance for a specific
underperforming category, without rebuilding all 15 categories.

Usage:
    python backend/scripts/build_memory_bank_for_category.py capsule 0.25
"""

import sys
from pathlib import Path

from app.core.categories import MVTEC_ROOT
from app.core.config import PROJECT_ROOT
from app.preprocessing.dataloader_factory import get_train_dataloader
from app.anomaly_detection.patchcore import PatchCore

MODELS_DIR = PROJECT_ROOT / "models"


def main():
    if len(sys.argv) != 3:
        print("Usage: python build_memory_bank_for_category.py <category> <subsample_ratio>")
        sys.exit(1)

    category = sys.argv[1]
    subsample_ratio = float(sys.argv[2])

    category_root = MVTEC_ROOT / category
    if not (category_root / "train" / "good").exists():
        print(f"No training data found for '{category}' at {category_root}")
        sys.exit(1)

    print(f"Building memory bank for '{category}' with subsample_ratio={subsample_ratio}")
    dataloader = get_train_dataloader(category_root, batch_size=8)
    patchcore = PatchCore(subsample_ratio=subsample_ratio)
    patchcore.fit(dataloader)

    output_path = MODELS_DIR / f"{category}_memory_bank.pt"
    patchcore.save(str(output_path))
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()