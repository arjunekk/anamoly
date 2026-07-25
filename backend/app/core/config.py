"""
Centralized application configuration.

Purpose: paths and settings that multiple modules need (model path,
upload directory, etc.) should live in one place, not be hardcoded
as string literals scattered across route handlers and pipeline code.
This is the first thing to change if the project structure ever moves
(e.g. deploying to a server with different folder paths).
"""

from pathlib import Path

# Project root, resolved relative to this file's location,
# so paths work correctly regardless of where the app is launched from.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "models" / "bottle_memory_bank.pt"
UPLOAD_DIR = PROJECT_ROOT / "reports" / "uploads"
HEATMAP_DIR = PROJECT_ROOT / "reports" / "heatmaps"

# Ensure these folders exist at import time, so routes never fail
# because a folder was missing.
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
HEATMAP_DIR.mkdir(parents=True, exist_ok=True)