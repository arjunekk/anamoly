"""
Tests for severity estimation and the recommendation engine (Phase 8,
extended in the multi-category phase for per-category threshold behavior).

These are pure unit tests — no model loading, no I/O — so they run
near-instantly and should be run constantly during development.
"""

from app.severity.severity_estimator import estimate_severity, Severity, get_thresholds_for_category
from app.recommendation.recommendation_engine import get_recommendations


def test_score_below_ceiling_is_none():
    assert estimate_severity(27.77) == Severity.NONE


def test_score_at_none_ceiling_is_none():
    """Boundary check: exactly at the threshold should still be NONE (inclusive)."""
    assert estimate_severity(32.38) == Severity.NONE


def test_score_just_above_none_ceiling_is_minor():
    assert estimate_severity(32.39) == Severity.MINOR


def test_score_in_moderate_range():
    assert estimate_severity(44.21) == Severity.MODERATE


def test_score_above_critical_threshold():
    assert estimate_severity(60.79) == Severity.CRITICAL


def test_known_edge_case_contamination_scores_as_none():
    """
    Documents the known false-negative case from calibration (see
    docs/calibration_notes.md): a real contamination defect scoring 29.59
    is classified as NONE. This test doesn't assert 'correct' behavior —
    it documents ACTUAL behavior, so if this classification logic ever
    changes, this test forces a conscious decision about whether that's
    intentional.
    """
    assert estimate_severity(29.59) == Severity.NONE


def test_none_severity_gives_no_action_recommendation():
    recommendations = get_recommendations(Severity.NONE)
    assert "No action required." in recommendations


def test_critical_severity_includes_immediate_rejection():
    recommendations = get_recommendations(Severity.CRITICAL)
    assert "Reject product immediately." in recommendations


def test_every_severity_level_returns_at_least_one_recommendation():
    for severity in Severity:
        recommendations = get_recommendations(severity)
        assert len(recommendations) > 0


def test_bottle_thresholds_unchanged_from_manual_calibration():
    """
    Confirms bottle still uses the original Phase 8 hand-calibrated
    thresholds, not a recomputed percentile version — this was an
    explicit design decision when multi-category support was added.
    """
    thresholds = get_thresholds_for_category("bottle")
    assert thresholds["none_ceiling"] == 32.38
    assert thresholds["minor_ceiling"] == 42.0
    assert thresholds["moderate_ceiling"] == 50.0


def test_different_categories_can_have_different_thresholds():
    """
    Sanity check that per-category calibration actually produced
    different thresholds for at least one other category vs bottle —
    if this ever fails, it likely means the calibration script didn't
    run or its output wasn't picked up correctly.
    """
    bottle_thresholds = get_thresholds_for_category("bottle")
    pill_thresholds = get_thresholds_for_category("pill")
    assert bottle_thresholds != pill_thresholds


def test_unknown_category_falls_back_to_bottle_thresholds():
    thresholds = get_thresholds_for_category("nonexistent_category")
    assert thresholds == get_thresholds_for_category("bottle")