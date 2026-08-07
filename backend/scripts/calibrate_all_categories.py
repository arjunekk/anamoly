"""
Automated severity threshold calibration across all available categories,
using percentile-based splitting of defective scores (see conversation
discussion — a scalable generalization of the manual process used for
bottle in Phase 8).

Outputs:
  - backend/app/core/severity_thresholds.json  (used by severity_estimator.py)
  - docs/calibration_notes_all_categories.md   (human-readable report)
"""

import json
import numpy as np
from pathlib import Path

from app.core.categories import get_available_categories, MVTEC_ROOT
from app.core.config import PROJECT_ROOT
from app.anomaly_detection.patchcore import PatchCore
from app.anomaly_detection.inference import run_inference

MODELS_DIR = PROJECT_ROOT / "models"
THRESHOLDS_PATH = PROJECT_ROOT / "backend" / "app" / "core" / "severity_thresholds.json"
REPORT_PATH = PROJECT_ROOT / "docs" / "calibration_notes_all_categories.md"


def collect_test_scores(category: str, patchcore: PatchCore) -> dict:
    """Runs inference across every test image, grouped by defect type."""
    test_root = MVTEC_ROOT / category / "test"
    scores_by_class = {}

    for class_folder in sorted(test_root.iterdir()):
        if not class_folder.is_dir():
            continue
        scores = []
        for image_path in sorted(class_folder.iterdir()):
            if image_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue
            result = run_inference(image_path, patchcore)
            scores.append(result["anomaly_score"])
        scores_by_class[class_folder.name] = scores

    return scores_by_class


def calibrate_category(category: str) -> dict:
    model_path = MODELS_DIR / f"{category}_memory_bank.pt"
    if not model_path.exists():
        print(f"Skipping {category}: no memory bank found at {model_path}")
        return None

    print(f"\n=== Calibrating: {category} ===")
    patchcore = PatchCore(subsample_ratio=0.1)
    patchcore.load(str(model_path))

    scores_by_class = collect_test_scores(category, patchcore)

    good_scores = scores_by_class.get("good", [])
    defective_scores = [
        score
        for class_name, scores in scores_by_class.items()
        if class_name != "good"
        for score in scores
    ]

    if not good_scores or not defective_scores:
        print(f"Skipping {category}: missing good or defective test scores")
        return None

    none_ceiling = float(np.percentile(good_scores, 95))
    minor_ceiling = float(np.percentile(defective_scores, 33))
    moderate_ceiling = float(np.percentile(defective_scores, 66))

    # Guard against a degenerate case: if percentile boundaries end up
    # below the good-image ceiling (possible for categories with heavy
    # good/defective overlap), push them up so the tiers stay ordered.
    minor_ceiling = max(minor_ceiling, none_ceiling + 0.01)
    moderate_ceiling = max(moderate_ceiling, minor_ceiling + 0.01)

    thresholds = {
        "none_ceiling": round(none_ceiling, 2),
        "minor_ceiling": round(minor_ceiling, 2),
        "moderate_ceiling": round(moderate_ceiling, 2),
    }

    summary = {
        class_name: {
            "count": len(scores),
            "min": round(min(scores), 2),
            "max": round(max(scores), 2),
            "mean": round(sum(scores) / len(scores), 2),
        }
        for class_name, scores in scores_by_class.items()
    }

    return {"thresholds": thresholds, "summary": summary}


def write_report(all_results: dict):
    lines = ["# Automated Multi-Category Calibration\n"]
    lines.append(
        "Thresholds derived automatically via percentile-based splitting "
        "of defective test scores per category (33rd/66th percentile), "
        "with the 'none' ceiling set to each category's own max good-image "
        "score. See conversation history for full reasoning and trade-offs "
        "versus the manual approach used for bottle.\n"
    )

    for category, result in all_results.items():
        if result is None:
            lines.append(f"\n## {category}\n\n_Skipped — missing memory bank or test data._\n")
            continue

        lines.append(f"\n## {category}\n")
        lines.append("| Class | Count | Min | Max | Mean |")
        lines.append("|---|---|---|---|---|")
        for class_name, stats in result["summary"].items():
            lines.append(
                f"| {class_name} | {stats['count']} | {stats['min']} | {stats['max']} | {stats['mean']} |"
            )
        t = result["thresholds"]
        lines.append(
            f"\n**Thresholds:** None ≤ {t['none_ceiling']} | "
            f"Minor ≤ {t['minor_ceiling']} | Moderate ≤ {t['moderate_ceiling']} | Critical above\n"
        )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")


def main():
    categories = get_available_categories()
    print(f"Calibrating {len(categories)} categories: {categories}")

    all_results = {}
    thresholds_json = {}

    for category in categories:
        result = calibrate_category(category)
        all_results[category] = result
        if result is not None:
            thresholds_json[category] = result["thresholds"]

    THRESHOLDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(THRESHOLDS_PATH, "w") as f:
        json.dump(thresholds_json, f, indent=2)
    print(f"\nThresholds saved to {THRESHOLDS_PATH}")

    write_report(all_results)


if __name__ == "__main__":
    main()