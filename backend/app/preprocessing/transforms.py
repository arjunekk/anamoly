"""
Image preprocessing transforms.

These transforms convert raw images into normalized tensors suitable
for WideResNet50-2. Kept in its own module (separate from the dataset
loader) so preprocessing logic can be reused during both training-time
loading (Phase 3) and inference-time loading (Phase 7), without duplication.
"""

from torchvision import transforms

# WideResNet50-2 is pretrained on ImageNet, so inputs must match
# the exact normalization statistics ImageNet models expect.
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# MVTec images vary in size; PatchCore commonly uses 224x224,
# matching standard ImageNet-pretrained input resolution.
IMAGE_SIZE = 224


def get_transform():
    """
    Returns the standard preprocessing pipeline:
    resize -> convert to tensor -> normalize with ImageNet stats.
    """
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])