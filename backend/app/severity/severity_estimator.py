"""
Converts a raw PatchCore anomaly score into a severity label.

Thresholds below were derived empirically from calibrating against the
full MVTec AD 'bottle' test set (see backend/tests/calibrate_thresholds.py),
not chosen arbitrarily. They reflect the actual score distribution observed:
good images topped out at ~32.4, while defective images clustered from
~37 to ~61. See docs/calibration_notes.md for the full data and discussion
of known limitations (e.g. subtle contamination defects can score close
to the 'good' range).
"""

from enum import Enum


class Severity(str, Enum):
    NONE = "none"
    MINOR = "minor"
    MODERATE = "moderate"
    CRITICAL = "critical"


# Thresholds calibrated from real test data — see module docstring.
NO_DEFECT_CEILING = 32.38
MINOR_CEILING = 42.0
MODERATE_CEILING = 50.0


def estimate_severity(anomaly_score: float) -> Severity:
    """
    Args:
        anomaly_score: raw PatchCore image-level anomaly score.

    Returns:
        A Severity enum value.
    """
    if anomaly_score <= NO_DEFECT_CEILING:
        return Severity.NONE
    elif anomaly_score <= MINOR_CEILING:
        return Severity.MINOR
    elif anomaly_score <= MODERATE_CEILING:
        return Severity.MODERATE
    else:
        return Severity.CRITICAL