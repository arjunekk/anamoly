"""
Feature extraction using a pretrained WideResNet50-2 backbone.

PatchCore uses intermediate feature maps (not final classification output)
from mid-level layers, since these capture local texture/structure at a
spatial resolution fine enough to localize small defects. The network's
weights are frozen — we are not training this model, only using it as a
fixed feature extractor.
"""

import torch
import torch.nn as nn
from torchvision.models import wide_resnet50_2, Wide_ResNet50_2_Weights


class WideResNetFeatureExtractor(nn.Module):
    """
    Extracts intermediate feature maps from layer2 and layer3 of a
    pretrained WideResNet50-2, following the standard PatchCore approach.
    """

    def __init__(self):
        super().__init__()

        # Load pretrained weights (trained on ImageNet)
        weights = Wide_ResNet50_2_Weights.IMAGENET1K_V2
        backbone = wide_resnet50_2(weights=weights)

        # Freeze all weights: we are not fine-tuning this network,
        # only using it to extract fixed features.
        for param in backbone.parameters():
            param.requires_grad = False

        # Keep the model in eval mode permanently (disables dropout/batchnorm updates)
        backbone.eval()

        # Break the backbone into named stages so we can capture
        # intermediate outputs, rather than only the final layer.
        self.stem = nn.Sequential(
            backbone.conv1,
            backbone.bn1,
            backbone.relu,
            backbone.maxpool,
        )
        self.layer1 = backbone.layer1
        self.layer2 = backbone.layer2
        self.layer3 = backbone.layer3
        # layer4 and the final classifier are intentionally unused —
        # PatchCore does not need them.

    @torch.no_grad()
    def forward(self, x: torch.Tensor):
        """
        Args:
            x: input batch of shape [batch_size, 3, 224, 224]

        Returns:
            A tuple (feat_layer2, feat_layer3) — intermediate feature maps
            used by PatchCore for anomaly detection.
        """
        x = self.stem(x)
        x = self.layer1(x)
        feat_layer2 = self.layer2(x)
        feat_layer3 = self.layer3(feat_layer2)

        return feat_layer2, feat_layer3