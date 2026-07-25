# Severity Threshold Calibration

## Method
Thresholds were derived by running PatchCore inference across the entire
MVTec AD 'bottle' test set (83 images: 20 good, 63 defective across three
defect types) and examining the actual distribution of anomaly scores,
rather than choosing arbitrary cutoffs.

## Observed Score Distribution

| Category      | Count | Min   | Max   | Mean  |
|---------------|-------|-------|-------|-------|
| broken_large  | 20    | 40.55 | 49.99 | 44.21 |
| broken_small  | 22    | 37.20 | 46.52 | 42.53 |
| contamination | 21    | 29.59 | 60.79 | 42.01 |
| good          | 20    | 23.84 | 32.38 | 27.77 |

## Chosen Thresholds

- **None:** score ≤ 32.38 (matches observed good-image ceiling)
- **Minor:** 32.38 – 42.0
- **Moderate:** 42.0 – 50.0
- **Critical:** > 50.0

## Known Limitation

One `contamination` sample scored 29.59 — inside the range of scores
observed for defect-free images. This reflects a real limitation of the
patch-distance approach: subtle textural defects (e.g. faint contamination)
are harder to separate from normal variation than structural defects
(e.g. cracks or breaks), which showed no overlap with good-image scores.

## Future Work
If additional product categories are added, thresholds should be
recalibrated per category using the same method, since "normal"
appearance varies significantly between product types.

## Confirmed Edge Case Behavior

Verified via backend/tests/test_severity_and_recommendations.py:

- A contamination sample scoring 29.59 is classified as **Severity.NONE**
  ("no defect detected"), despite being a genuine defect in the ground truth.
  This is a confirmed false negative — the current threshold-based system
  will occasionally miss subtle contamination defects.

## Implication for Production Use

This system is a portfolio/demonstration project and this limitation should
be disclosed, not hidden. A production deployment would likely need:
- Per-category threshold tuning with a larger calibration set
- A secondary check (e.g. lower "review" threshold that flags borderline
  scores for human inspection rather than auto-passing them)
- Possibly a different anomaly detection approach for texture-based defects
  specifically, since PatchCore's patch-distance method separates
  structural defects (cracks, breaks) more reliably than subtle textural
  ones (contamination)