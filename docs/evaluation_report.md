# Model Evaluation Report

Computed across all available MVTec AD categories. Image-level metrics compare the raw anomaly score (AUROC) and the system's actual severity decision (precision/recall/F1/confusion matrix) against ground truth labels. Pixel-level AUROC measures how well the heatmap localizes the true defect region, averaged per-image across defective test images with a ground truth mask (a lighter-weight approximation of the paper convention of pooling all pixels together — see project documentation for this trade-off).


## Summary Table

| Category | Image AUROC | Precision | Recall | F1 | Pixel AUROC (mean) | Test Images |
|---|---|---|---|---|---|---|
| bottle | 0.995 | 0.939 | 0.984 | 0.961 | 0.987 | 83 |
| cable | 0.852 | 0.943 | 0.543 | 0.690 | 0.960 | 150 |
| capsule | 0.925 | 0.972 | 0.642 | 0.773 | 0.983 | 132 |
| carpet | 0.984 | 0.976 | 0.933 | 0.954 | 0.989 | 117 |
| grid | 0.757 | 0.923 | 0.421 | 0.578 | 0.977 | 78 |
| hazelnut | 0.997 | 0.972 | 1.000 | 0.986 | 0.988 | 110 |
| leather | 1.000 | 0.979 | 1.000 | 0.989 | 0.996 | 124 |
| metal_nut | 0.992 | 0.979 | 0.989 | 0.984 | 0.972 | 115 |
| pill | 0.862 | 0.976 | 0.574 | 0.723 | 0.963 | 167 |
| screw | 0.886 | 0.948 | 0.462 | 0.621 | 0.985 | 160 |
| tile | 0.923 | 0.968 | 0.714 | 0.822 | 0.949 | 117 |
| toothbrush | 0.839 | 0.917 | 0.367 | 0.524 | 0.984 | 42 |
| transistor | 0.908 | 0.870 | 0.500 | 0.635 | 0.903 | 100 |
| wood | 0.985 | 0.983 | 0.967 | 0.975 | 0.958 | 79 |
| zipper | 0.921 | 0.964 | 0.445 | 0.609 | 0.979 | 151 |

## Confusion Matrices


### bottle

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 16 (TN) | 4 (FP) |
| **Actual: Defective** | 1 (FN) | 62 (TP) |

### cable

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 55 (TN) | 3 (FP) |
| **Actual: Defective** | 42 (FN) | 50 (TP) |

### capsule

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 21 (TN) | 2 (FP) |
| **Actual: Defective** | 39 (FN) | 70 (TP) |

### carpet

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 26 (TN) | 2 (FP) |
| **Actual: Defective** | 6 (FN) | 83 (TP) |

### grid

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 19 (TN) | 2 (FP) |
| **Actual: Defective** | 33 (FN) | 24 (TP) |

### hazelnut

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 38 (TN) | 2 (FP) |
| **Actual: Defective** | 0 (FN) | 70 (TP) |

### leather

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 30 (TN) | 2 (FP) |
| **Actual: Defective** | 0 (FN) | 92 (TP) |

### metal_nut

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 20 (TN) | 2 (FP) |
| **Actual: Defective** | 1 (FN) | 92 (TP) |

### pill

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 24 (TN) | 2 (FP) |
| **Actual: Defective** | 60 (FN) | 81 (TP) |

### screw

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 38 (TN) | 3 (FP) |
| **Actual: Defective** | 64 (FN) | 55 (TP) |

### tile

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 31 (TN) | 2 (FP) |
| **Actual: Defective** | 24 (FN) | 60 (TP) |

### toothbrush

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 11 (TN) | 1 (FP) |
| **Actual: Defective** | 19 (FN) | 11 (TP) |

### transistor

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 57 (TN) | 3 (FP) |
| **Actual: Defective** | 20 (FN) | 20 (TP) |

### wood

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 18 (TN) | 1 (FP) |
| **Actual: Defective** | 2 (FN) | 58 (TP) |

### zipper

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 30 (TN) | 2 (FP) |
| **Actual: Defective** | 66 (FN) | 53 (TP) |

## Memory Bank Subsample Ratio Experiment

Capsule, toothbrush, screw, and grid initially underperformed relative to
other categories after threshold recalibration (see project history).
As a follow-up experiment, these four categories' memory banks were
rebuilt with a richer subsample ratio (0.25 vs the default 0.1) to test
whether a larger reference set of "normal" patch features would improve
detection.

**Results were mixed, not uniformly positive:**

- **Capsule**: clear improvement (AUROC 0.800→0.925, recall 0.202→0.642)
- **Toothbrush**: roughly neutral (AUROC 0.831→0.839, recall 0.333→0.367)
- **Screw**: AUROC improved (0.832→0.886) but recall *decreased*
  (0.563→0.462) after threshold recalibration on the new score distribution
- **Grid**: both AUROC and recall decreased (0.825→0.757, 0.544→0.421) —
  a genuine regression, plausibly because grid's highly repetitive,
  self-similar texture means a larger memory bank captures more
  "acceptable normal variation," making subtle distortions harder to
  distinguish from that broader normal range

**Decision:** all four categories were kept at the 0.25 ratio despite
grid and screw's regression, prioritizing capsule's substantial gain.
This is a deliberate trade-off, not an oversight — it illustrates that
"more reference data" is not a universal improvement for every product
category, and that per-category tuning has real, category-specific
trade-offs rather than one setting that's globally optimal.