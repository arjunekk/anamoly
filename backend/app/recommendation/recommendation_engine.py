"""
Rule-based maintenance recommendation engine.

Deliberately simple and rule-based per project scope — maps a severity
level to a list of recommended actions. Designed to be swappable: a
future ML/LLM-based engine only needs to implement the same
`get_recommendations(severity) -> list[str]` interface to be a drop-in
replacement, without touching any other module.
"""

from app.severity.severity_estimator import Severity


RECOMMENDATION_RULES: dict[Severity, list[str]] = {
    Severity.NONE: [
        "No action required.",
        "Product passed inspection.",
    ],
    Severity.MINOR: [
        "Flag product for manual secondary review.",
        "Log occurrence for trend monitoring.",
    ],
    Severity.MODERATE: [
        "Reject product.",
        "Inspect relevant production line station.",
        "Schedule routine maintenance check.",
    ],
    Severity.CRITICAL: [
        "Reject product immediately.",
        "Inspect conveyor alignment.",
        "Recalibrate machine.",
        "Schedule urgent maintenance.",
    ],
}


def get_recommendations(severity: Severity) -> list[str]:
    """
    Args:
        severity: a Severity enum value.

    Returns:
        A list of recommended maintenance actions for that severity level.
    """
    return RECOMMENDATION_RULES.get(severity, ["No recommendation available."])