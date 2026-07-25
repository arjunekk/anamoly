"""
End-to-end verification of PatchCore.

Purpose: Build a memory bank from training data, then run inference on
one known-good and one known-defective test image, confirming the
defective image produces a meaningfully higher anomaly score.
"""

from pathlib import Path
import torch
from PIL import Image

from app.preprocessing.dataloader_factory import get_train_dataloader
from app.preprocessing.transforms import get_transform
from app.anomaly_detection.patchcore import PatchCore

CATEGORY_ROOT = Path("dataset/mvtec_ad/bottle")
MODEL_SAVE_PATH = "models/bottle_memory_bank.pt"


def load_single_image(path: Path) -> torch.Tensor:
    """Load and preprocess a single image into a [1, 3, 224, 224] tensor."""
    image = Image.open(path).convert("RGB")
    transform = get_transform()
    tensor = transform(image)
    return tensor.unsqueeze(0)  # add batch dimension


def main():
    # Step 1: Build the memory bank from training data.
    train_loader = get_train_dataloader(CATEGORY_ROOT, batch_size=8)
    patchcore = PatchCore(subsample_ratio=0.1)

    print("Building memory bank from training images...")
    patchcore.fit(train_loader)
    patchcore.save(MODEL_SAVE_PATH)

    # Step 2: Test on one good image.
    good_image_path = CATEGORY_ROOT / "test" / "good" / "000.png"
    good_tensor = load_single_image(good_image_path)
    good_score, _ = patchcore.predict(good_tensor)

    # Step 3: Test on one defective image.
    defect_image_path = CATEGORY_ROOT / "test" / "broken_large" / "000.png"
    defect_tensor = load_single_image(defect_image_path)
    defect_score, _ = patchcore.predict(defect_tensor)

    print(f"\nGood image anomaly score:      {good_score:.4f}")
    print(f"Defective image anomaly score: {defect_score:.4f}")

    if defect_score > good_score:
        print("\n✅ Defective image correctly scored higher than good image.")
    else:
        print("\n⚠️  Unexpected: defective image did not score higher. Investigate.")


if __name__ == "__main__":
    main()