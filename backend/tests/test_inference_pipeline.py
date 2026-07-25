"""
Verification script for the full inference pipeline.

Purpose: Load a previously saved memory bank (no rebuilding), run
inference on one good and one defective image, and save the heatmap
overlays to disk for visual inspection.
"""

from pathlib import Path
from app.anomaly_detection.patchcore import PatchCore
from app.anomaly_detection.inference import run_inference

CATEGORY_ROOT = Path("dataset/mvtec_ad/bottle")
MODEL_PATH = "models/bottle_memory_bank.pt"


def main():
    patchcore = PatchCore(subsample_ratio=0.1)
    patchcore.load(MODEL_PATH)

    good_image_path = CATEGORY_ROOT / "test" / "good" / "000.png"
    defect_image_path = CATEGORY_ROOT / "test" / "broken_large" / "000.png"

    good_result = run_inference(good_image_path, patchcore)
    defect_result = run_inference(defect_image_path, patchcore)

    print(f"Good image score:      {good_result['anomaly_score']:.4f}")
    print(f"Defective image score: {defect_result['anomaly_score']:.4f}")

    good_result["heatmap_image"].save("backend/tests/good_heatmap.png")
    defect_result["heatmap_image"].save("backend/tests/defect_heatmap.png")

    print("\nSaved heatmap overlays to backend/tests/good_heatmap.png and defect_heatmap.png")


if __name__ == "__main__":
    main()