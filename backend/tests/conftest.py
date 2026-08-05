"""
Shared pytest fixtures for the test suite.

conftest.py is auto-discovered by pytest — fixtures defined here are
available to every test file in this folder without needing to import
them explicitly.
"""

import pytest
from pathlib import Path

from app.anomaly_detection.patchcore import PatchCore

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CATEGORY_ROOT = PROJECT_ROOT / "dataset" / "mvtec_ad" / "bottle"
MODEL_PATH = PROJECT_ROOT / "models" / "bottle_memory_bank.pt"


@pytest.fixture(scope="session")
def loaded_patchcore():
    """
    Loads the PatchCore model with its memory bank once per test session
    (not once per test) — loading is slow, and every test that needs the
    model can just reuse this same instance.
    """
    if not MODEL_PATH.exists():
        pytest.skip(f"Memory bank not found at {MODEL_PATH}. Run test_patchcore.py first.")

    pc = PatchCore(subsample_ratio=0.1)
    pc.load(str(MODEL_PATH))
    return pc


@pytest.fixture
def good_image_path():
    return CATEGORY_ROOT / "test" / "good" / "000.png"


@pytest.fixture
def defective_image_path():
    return CATEGORY_ROOT / "test" / "broken_large" / "000.png"


@pytest.fixture
def category_root():
    return CATEGORY_ROOT