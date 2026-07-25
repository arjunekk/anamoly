"""
Combines layer2 and layer3 feature maps into a single set of patch-level
feature vectors, as used by PatchCore.

layer2 and layer3 have different spatial resolutions (28x28 vs 14x14).
We upsample layer3 to match layer2's resolution, then concatenate along
the channel dimension so each spatial location has one combined descriptor.
"""

import torch
import torch.nn.functional as F


def aggregate_patch_features(feat_layer2: torch.Tensor, feat_layer3: torch.Tensor) -> torch.Tensor:
    """
    Args:
        feat_layer2: shape [B, 512, 28, 28]
        feat_layer3: shape [B, 1024, 14, 14]

    Returns:
        Patch feature tensor of shape [B, 28*28, 1536] —
        one 1536-dim feature vector per spatial patch, per image.
    """
    target_size = feat_layer2.shape[-2:]  # (28, 28)

    # Upsample layer3 to match layer2's spatial resolution.
    feat_layer3_upsampled = F.interpolate(
        feat_layer3, size=target_size, mode="bilinear", align_corners=False
    )

    # Concatenate along channel dimension: 512 + 1024 = 1536 channels.
    combined = torch.cat([feat_layer2, feat_layer3_upsampled], dim=1)

    batch_size, channels, height, width = combined.shape

    # Reshape from [B, C, H, W] to [B, H*W, C] — one row per patch.
    patch_features = combined.permute(0, 2, 3, 1).reshape(batch_size, height * width, channels)

    return patch_features