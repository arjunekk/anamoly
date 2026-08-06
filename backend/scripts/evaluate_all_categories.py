"""
Full evaluation across all available categories: image-level AUROC,
confusion matrix, precision/recall/F1 (using each category's calibrated
severity threshold), and pixel-level localization AUROC against ground
truth masks.

Outputs:
  - docs/evaluation_results.json  (raw numbers, all categories)
  - docs/evaluation_report.md     (human-readable summary + confusion matrices)
"""

import json
from pathlib import Path
from PIL import Image

from app.core.categories import get_available_categories, MVTEC_ROOT
from app.core.config import PROJECT_ROOT
from app.preprocessing.transforms import get_transform
from app.anomaly_detection.patchcore import PatchCore
from app.severity.severity_estimator import estimate_severity, Severity
from app.evaluation.metrics import compute_image_level_metrics, compute_pixel_level_auroc

MODELS_DIR = PROJECT_ROOT / "models"
REPORT_JSON_PATH = PROJECT_ROOT / "docs" / "evaluation_results.json"
REPORT_MD_PATH = PROJECT_ROOT / "docs" / "evaluation_report.md"


def load_tensor(image_path):
    image = Image.open(image_path).convert("RGB")
    transform = get_transform()
    tensor = transform(image).unsqueeze(0)
    return tensor, image.size  # (width, height)


def evaluate_category(category: str):
    model_path = MODELS_DIR / f"{category}_memory_bank.pt"
    if not model_path.exists():
        print(f"Skipping {category}: no memory bank")
        return None

    print(f"\n=== Evaluating: {category} ===")
    patchcore = PatchCore(subsample_ratio=0.1)
    patchcore.load(str(model_path))

    test_root = MVTEC_ROOT / category / "test"
    ground_truth_root = MVTEC_ROOT / category / "ground_truth"

    y_true, y_scores, y_pred_defective = [], [], []
    pixel_aurocs = []

    for class_folder in sorted(test_root.iterdir()):
        if not class_folder.is_dir():
            continue
        is_defective_class = class_folder.name != "good"

        for image_path in sorted(class_folder.iterdir()):
            if image_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue

            tensor, original_size = load_tensor(image_path)
            score, heatmap = patchcore.predict(tensor)

            y_true.append(1 if is_defective_class else 0)
            y_scores.append(score)

            severity = estimate_severity(score, category=category)
            y_pred_defective.append(0 if severity == Severity.NONE else 1)

            if is_defective_class:
                mask_path = ground_truth_root / class_folder.name / f"{image_path.stem}_mask.png"
                if mask_path.exists():
                    pixel_auroc = compute_pixel_level_auroc(heatmap, mask_path, original_size)
                    if pixel_auroc is not None:
                        pixel_aurocs.append(pixel_auroc)

    image_metrics = compute_image_level_metrics(y_true, y_scores, y_pred_defective)
    avg_pixel_auroc = sum(pixel_aurocs) / len(pixel_aurocs) if pixel_aurocs else None

    return {
        "image_level": image_metrics,
        "pixel_level_auroc_mean": avg_pixel_auroc,
        "pixel_level_auroc_count": len(pixel_aurocs),
        "num_test_images": len(y_true),
    }


def write_markdown_report(all_results: dict):
    lines = ["# Model Evaluation Report\n"]
    lines.append(
        "Computed across all available MVTec AD categories. Image-level "
        "metrics compare the raw anomaly score (AUROC) and the system's "
        "actual severity decision (precision/recall/F1/confusion matrix) "
        "against ground truth labels. Pixel-level AUROC measures how well "
        "the heatmap localizes the true defect region, averaged per-image "
        "across defective test images with a ground truth mask (a lighter-"
        "weight approximation of the paper convention of pooling all pixels "
        "together — see project documentation for this trade-off).\n"
    )

    lines.append("\n## Summary Table\n")
    lines.append("| Category | Image AUROC | Precision | Recall | F1 | Pixel AUROC (mean) | Test Images |")
    lines.append("|---|---|---|---|---|---|---|")

    for category, result in all_results.items():
        if result is None:
            lines.append(f"| {category} | — | — | — | — | — | skipped |")
            continue
        im = result["image_level"]
        auroc_str = f"{im['auroc']:.3f}" if im["auroc"] is not None else "N/A"
        pixel_str = (
            f"{result['pixel_level_auroc_mean']:.3f}"
            if result["pixel_level_auroc_mean"] is not None
            else "N/A"
        )
        lines.append(
            f"| {category} | {auroc_str} | {im['precision']:.3f} | {im['recall']:.3f} | "
            f"{im['f1']:.3f} | {pixel_str} | {result['num_test_images']} |"
        )

    lines.append("\n## Confusion Matrices\n")
    for category, result in all_results.items():
        if result is None:
            continue
        im = result["image_level"]
        lines.append(f"\n### {category}\n")
        lines.append("| | Predicted: No Defect | Predicted: Defect |")
        lines.append("|---|---|---|")
        lines.append(f"| **Actual: Good** | {im['true_negatives']} (TN) | {im['false_positives']} (FP) |")
        lines.append(f"| **Actual: Defective** | {im['false_negatives']} (FN) | {im['true_positives']} (TP) |")

    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nMarkdown report written to {REPORT_MD_PATH}")


def main():
    categories = get_available_categories()
    print(f"Evaluating {len(categories)} categories")

    all_results = {}
    for category in categories:
        all_results[category] = evaluate_category(category)

    REPORT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_JSON_PATH, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nRaw results saved to {REPORT_JSON_PATH}")

    write_markdown_report(all_results)


if __name__ == "__main__":
    main()