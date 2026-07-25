"""
Visualize one defective test image alongside its ground truth mask.

Purpose: Confirm that images and masks are correctly paired and that
mask pixels genuinely correspond to the defective region — before we
build any preprocessing or model code that assumes this pairing.
"""

import cv2
import random
import matplotlib.pyplot as plt
from pathlib import Path


DATASET_ROOT = Path("dataset/mvtec_ad/bottle")

# Pick one known defective category to inspect
DEFECT_TYPE = "broken_large"
IMAGE_INDEX = f"{random.randint(0, 15):03d}"  # MVTec filenames are zero-padded, e.g. 000.png


def load_image(path: Path):
    """Load an image in RGB (OpenCV loads BGR by default)."""
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"Could not read image at: {path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def load_mask(path: Path):
    """Load a ground truth mask as grayscale."""
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(f"Could not read mask at: {path}")
    return mask


def main():
    image_path = DATASET_ROOT / "test" / DEFECT_TYPE / f"{IMAGE_INDEX}.png"
    mask_path = DATASET_ROOT / "ground_truth" / DEFECT_TYPE / f"{IMAGE_INDEX}_mask.png"

    image = load_image(image_path)
    mask = load_mask(mask_path)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(image)
    axes[0].set_title(f"Defective Image ({DEFECT_TYPE})")
    axes[0].axis("off")

    axes[1].imshow(mask, cmap="gray")
    axes[1].set_title("Ground Truth Mask")
    axes[1].axis("off")

    plt.tight_layout()
    plt.savefig("backend/tests/sample_inspection.png")
    print("Saved comparison to backend/tests/sample_inspection.png")


if __name__ == "__main__":
    main()