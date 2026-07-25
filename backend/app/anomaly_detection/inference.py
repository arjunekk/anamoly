"""
End-to-end inference pipeline: takes a raw image and a pre-built PatchCore
model, and returns an anomaly score plus a rendered heatmap overlay.

This is the exact function Phase 9's API endpoint will call — everything
before this phase was building and validating the pieces; this phase
assembles them into the single entry point the rest of the system uses.
"""

from pathlib import Path
from PIL import Image

from app.preprocessing.transforms import get_transform
from app.anomaly_detection.patchcore import PatchCore
from app.anomaly_detection.heatmap_renderer import render_heatmap_overlay


def run_inference(image_path: Path, patchcore: PatchCore):
    """
    Args:
        image_path: path to the uploaded image.
        patchcore: a PatchCore instance with an already-loaded memory bank.

    Returns:
        dict with:
            - anomaly_score (float)
            - heatmap_image (PIL.Image) — original image with overlay
    """
    original_image = Image.open(image_path).convert("RGB")

    transform = get_transform()
    input_tensor = transform(original_image).unsqueeze(0)  # add batch dim

    anomaly_score, raw_heatmap = patchcore.predict(input_tensor)

    heatmap_overlay = render_heatmap_overlay(original_image, raw_heatmap)

    return {
        "anomaly_score": anomaly_score,
        "heatmap_image": heatmap_overlay,
    }