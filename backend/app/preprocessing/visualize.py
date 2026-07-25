"""
Utility to reverse ImageNet normalization for visual sanity checks.

Purpose: Confirm the preprocessing pipeline (resize -> tensor -> normalize)
is mathematically correct by reversing it and viewing the result. This is
a debugging/verification tool, not something used in the production pipeline.
"""

import torch
import numpy as np
from PIL import Image

from app.preprocessing.transforms import IMAGENET_MEAN, IMAGENET_STD


def unnormalize_tensor(tensor: torch.Tensor) -> Image.Image:
    """
    Reverses ImageNet normalization and converts a tensor back to a
    viewable PIL image.

    Args:
        tensor: normalized image tensor of shape [3, H, W]

    Returns:
        A PIL Image in standard 0-255 RGB format.
    """
    mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD).view(3, 1, 1)

    # Reverse: normalized = (original - mean) / std
    #       -> original  = normalized * std + mean
    unnormalized = tensor * std + mean

    # Clamp to valid range in case of small floating point overshoot
    unnormalized = torch.clamp(unnormalized, 0, 1)

    # Convert from [3, H, W] tensor to [H, W, 3] numpy array for PIL
    image_array = (unnormalized.permute(1, 2, 0).numpy() * 255).astype(np.uint8)

    return Image.fromarray(image_array)