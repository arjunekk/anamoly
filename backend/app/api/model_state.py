"""
Manages the single, shared PatchCore model instance for the running server.

Purpose: the memory bank must be loaded from disk exactly once, when the
server starts — not on every request. This module provides a simple
get/set interface so main.py can load the model at startup, and routes
can retrieve that same instance without reloading it.
"""

from app.anomaly_detection.patchcore import PatchCore

_patchcore_instance: PatchCore | None = None


def load_patchcore_model(model_path: str):
    """Loads the PatchCore model once and stores it for reuse. Called at server startup."""
    global _patchcore_instance
    _patchcore_instance = PatchCore(subsample_ratio=0.1)
    _patchcore_instance.load(model_path)
    print("PatchCore model loaded and ready.")


def get_patchcore_model() -> PatchCore:
    """Retrieves the already-loaded PatchCore instance. Raises if called before startup loading."""
    if _patchcore_instance is None:
        raise RuntimeError(
            "PatchCore model has not been loaded yet. "
            "Ensure load_patchcore_model() is called during server startup."
        )
    return _patchcore_instance