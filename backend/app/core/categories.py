"""
Registry of supported MVTec AD product categories.

Centralizing this list means every script (memory bank building,
calibration, API loading) iterates over the same source of truth —
adding or removing a category means editing one list, not hunting
through multiple files.
"""

from pathlib import Path
from app.core.config import PROJECT_ROOT

MVTEC_ROOT = PROJECT_ROOT / "dataset" / "mvtec_ad"

ALL_CATEGORIES = [
    "bottle", "cable", "capsule", "carpet", "grid", "hazelnut",
    "leather", "metal_nut", "pill", "screw", "tile", "toothbrush",
    "transistor", "wood", "zipper",
]


def get_available_categories() -> list[str]:
    """
    Returns only the categories that actually have data downloaded on disk.
    Lets every script/route gracefully handle "not all 15 are present yet"
    instead of crashing if the user hasn't finished downloading everything.
    """
    return [
        cat for cat in ALL_CATEGORIES
        if (MVTEC_ROOT / cat / "train" / "good").exists()
    ]