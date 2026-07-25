"""
Calibration script: runs every image in the test set through PatchCore
and records anomaly scores grouped by ground-truth category.

Purpose: severity thresholds (Minor/Moderate/Critical) must be based on
the actual distribution of real anomaly scores, not arbitrary guesses.
This script produces that evidence before we hardcode any threshold.
"""

from pathlib import Path
from app.anomaly_detection.patchcore import PatchCore
from app.anomaly_detection.inference import run_inference

CATEGORY_ROOT = Path("dataset/mvtec_ad/bottle")
MODEL_PATH = "models/bottle_memory_bank.pt"


def main():
    patchcore = PatchCore(subsample_ratio=0.1)
    patchcore.load(MODEL_PATH)

    test_root = CATEGORY_ROOT / "test"
    results = {}

    for class_folder in sorted(test_root.iterdir()):
        if not class_folder.is_dir():
            continue

        scores = []
        image_paths = sorted(
            f for f in class_folder.iterdir()
            if f.suffix.lower() in {".png", ".jpg", ".jpeg"}
        )

        for image_path in image_paths:
            result = run_inference(image_path, patchcore)
            scores.append(result["anomaly_score"])

        results[class_folder.name] = scores

    print(f"{'Category':<20} {'Count':<8} {'Min':<10} {'Max':<10} {'Mean':<10}")
    print("-" * 60)
    for category, scores in results.items():
        print(
            f"{category:<20} {len(scores):<8} "
            f"{min(scores):<10.2f} {max(scores):<10.2f} "
            f"{sum(scores) / len(scores):<10.2f}"
        )


if __name__ == "__main__":
    main()