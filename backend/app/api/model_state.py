"""
Manages PatchCore model instances for every available category.

Each category has its own memory bank (bottle's "normal" looks nothing
like cable's "normal"), so this holds a dict keyed by category name,
all loaded once at server startup — not a single shared instance
like before multi-category support.
"""

from pathlib import Path
from app.anomaly_detection.patchcore import PatchCore
from app.core.categories import get_available_categories
from app.core.config import PROJECT_ROOT

MODELS_DIR = PROJECT_ROOT / "models"

_patchcore_models: dict[str, PatchCore] = {}


def load_all_patchcore_models():
    """
    Loads every available category's memory bank once, at server startup.
    Categories without a built memory bank yet are skipped with a warning,
    not a crash — lets the system run with a partial set of categories
    while others are still being downloaded/built.
    """
    categories = get_available_categories()

    for category in categories:
        model_path = MODELS_DIR / f"{category}_memory_bank.pt"
        if not model_path.exists():
            print(f"WARNING: no memory bank found for '{category}', skipping.")
            continue

        pc = PatchCore(subsample_ratio=0.1)
        pc.load(str(model_path))
        _patchcore_models[category] = pc
        print(f"Loaded model for category: {category}")

    print(f"PatchCore models ready for {len(_patchcore_models)} categories.")


def get_patchcore_model(category: str) -> PatchCore:
    if category not in _patchcore_models:
        raise ValueError(
            f"No model loaded for category '{category}'. "
            f"Available categories: {list(_patchcore_models.keys())}"
        )
    return _patchcore_models[category]


def get_loaded_categories() -> list[str]:
    """Used by the frontend to populate the category dropdown."""
    return list(_patchcore_models.keys())