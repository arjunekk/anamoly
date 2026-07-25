"""
Verification script for severity estimation and recommendation engine.

Purpose: Confirm both modules correctly classify a range of real anomaly
scores (from actual test images) into severity levels and recommendations,
before wiring this into the API (Phase 9).
"""

from app.severity.severity_estimator import estimate_severity
from app.recommendation.recommendation_engine import get_recommendations

# Sample scores pulled from the actual calibration run.
test_scores = {
    "good sample": 27.77,
    "borderline contamination": 29.59,
    "broken_small (min)": 37.20,
    "broken_large (mean)": 44.21,
    "contamination (max)": 60.79,
}


def main():
    for label, score in test_scores.items():
        severity = estimate_severity(score)
        recommendations = get_recommendations(severity)

        print(f"\n{label} (score={score})")
        print(f"  Severity: {severity.value}")
        print(f"  Recommendations:")
        for rec in recommendations:
            print(f"    - {rec}")


if __name__ == "__main__":
    main()