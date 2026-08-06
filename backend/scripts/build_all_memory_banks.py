"""
Builds and saves a PatchCore memory bank for every available category.

Replaces the one-off manual process from Phase 6 (which only handled
bottle) with a loop that scales to all categories automatically.
"""

from pathlib import Path
from app.core.categories import get_available_categories, MVTEC_ROOT
from app.core.config import PROJECT_ROOT
from app.preprocessing.dataloader_factory import get_train_dataloader
from app.anomaly_detection.patchcore import PatchCore

MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)


def build_memory_bank_for_category(category: str):
    print(f"\n=== Building memory bank: {category} ===")
    category_root = MVTEC_ROOT / category

    dataloader = get_train_dataloader(category_root, batch_size=8)
    patchcore = PatchCore(subsample_ratio=0.1)
    patchcore.fit(dataloader)

    output_path = MODELS_DIR / f"{category}_memory_bank.pt"
    patchcore.save(str(output_path))


def main():
    categories = get_available_categories()
    print(f"Found {len(categories)} categories with data: {categories}")

    for category in categories:
        build_memory_bank_for_category(category)

    print(f"\nDone. Built {len(categories)} memory banks.")


if __name__ == "__main__":
    main()