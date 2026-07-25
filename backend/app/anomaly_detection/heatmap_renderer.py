"""
Converts a raw 28x28 patch-distance heatmap into a viewable overlay
on the original image.

The raw heatmap from PatchCore is low-resolution (one value per patch,
not per pixel) and unitless (nearest-neighbor distances, not 0-255 colors).
This module handles both problems: upsampling to full image resolution,
and mapping distance values to a visual color scale.
"""

import numpy as np
import cv2
import torch
from PIL import Image


def render_heatmap_overlay(
    original_image: Image.Image,
    heatmap: torch.Tensor,
    alpha: float = 0.5,
) -> Image.Image:
    """
    Args:
        original_image: the original PIL image (any size).
        heatmap: raw per-patch distances, shape [28, 28].
        alpha: blend strength of the heatmap over the original image.

    Returns:
        A PIL image: original image with a color-mapped heatmap overlay.
    """
    original_np = np.array(original_image.convert("RGB"))
    target_h, target_w = original_np.shape[:2]

    heatmap_np = heatmap.numpy()

    # Normalize heatmap values to 0-255 for color mapping.
    # Min-max normalization here is a deliberate choice for VISUALIZATION
    # only — it makes each image's heatmap use the full color range for
    # clarity. It is NOT used for the anomaly score itself, which relies
    # on raw, unnormalized distances (Phase 6).
    normalized = heatmap_np - heatmap_np.min()
    max_val = normalized.max()
    if max_val > 0:
        normalized = normalized / max_val
    normalized = (normalized * 255).astype(np.uint8)

    # Upsample from 28x28 to the original image's resolution.
    upsampled = cv2.resize(normalized, (target_w, target_h), interpolation=cv2.INTER_CUBIC)

    # Apply a color map (JET: blue = low anomaly, red = high anomaly).
    color_heatmap = cv2.applyColorMap(upsampled, cv2.COLORMAP_JET)
    color_heatmap = cv2.cvtColor(color_heatmap, cv2.COLOR_BGR2RGB)

    # Blend the heatmap with the original image.
    blended = cv2.addWeighted(original_np, 1 - alpha, color_heatmap, alpha, 0)

    return Image.fromarray(blended)