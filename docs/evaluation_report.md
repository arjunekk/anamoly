# Model Evaluation Report

Computed across all available MVTec AD categories. Image-level metrics compare the raw anomaly score (AUROC) and the system's actual severity decision (precision/recall/F1/confusion matrix) against ground truth labels. Pixel-level AUROC measures how well the heatmap localizes the true defect region, averaged per-image across defective test images with a ground truth mask (a lighter-weight approximation of the paper convention of pooling all pixels together — see project documentation for this trade-off).


## Summary Table

| Category | Image AUROC | Precision | Recall | F1 | Pixel AUROC (mean) | Test Images |
|---|---|---|---|---|---|---|
| bottle | 0.995 | 0.939 | 0.984 | 0.961 | 0.987 | 83 |
| cable | 0.852 | 1.000 | 0.207 | 0.342 | 0.960 | 150 |
| capsule | 0.800 | 0.500 | 0.009 | 0.018 | 0.982 | 132 |
| carpet | 0.984 | 0.988 | 0.933 | 0.960 | 0.989 | 117 |
| grid | 0.825 | 0.947 | 0.316 | 0.474 | 0.969 | 78 |
| hazelnut | 0.997 | 1.000 | 0.914 | 0.955 | 0.988 | 110 |
| leather | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 124 |
| metal_nut | 0.992 | 0.989 | 0.957 | 0.973 | 0.972 | 115 |
| pill | 0.862 | 0.984 | 0.433 | 0.601 | 0.963 | 167 |
| screw | 0.832 | 0.857 | 0.050 | 0.095 | 0.983 | 160 |
| tile | 0.923 | 0.979 | 0.560 | 0.712 | 0.949 | 117 |
| toothbrush | 0.831 | 0.909 | 0.333 | 0.488 | 0.980 | 42 |
| transistor | 0.908 | 0.917 | 0.275 | 0.423 | 0.903 | 100 |
| wood | 0.985 | 0.982 | 0.900 | 0.939 | 0.958 | 79 |
| zipper | 0.921 | 1.000 | 0.336 | 0.503 | 0.979 | 151 |

## Confusion Matrices


### bottle

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 16 (TN) | 4 (FP) |
| **Actual: Defective** | 1 (FN) | 62 (TP) |

### cable

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 58 (TN) | 0 (FP) |
| **Actual: Defective** | 73 (FN) | 19 (TP) |

### capsule

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 22 (TN) | 1 (FP) |
| **Actual: Defective** | 108 (FN) | 1 (TP) |

### carpet

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 27 (TN) | 1 (FP) |
| **Actual: Defective** | 6 (FN) | 83 (TP) |

### grid

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 20 (TN) | 1 (FP) |
| **Actual: Defective** | 39 (FN) | 18 (TP) |

### hazelnut

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 40 (TN) | 0 (FP) |
| **Actual: Defective** | 6 (FN) | 64 (TP) |

### leather

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 32 (TN) | 0 (FP) |
| **Actual: Defective** | 0 (FN) | 92 (TP) |

### metal_nut

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 21 (TN) | 1 (FP) |
| **Actual: Defective** | 4 (FN) | 89 (TP) |

### pill

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 25 (TN) | 1 (FP) |
| **Actual: Defective** | 80 (FN) | 61 (TP) |

### screw

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 40 (TN) | 1 (FP) |
| **Actual: Defective** | 113 (FN) | 6 (TP) |

### tile

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 32 (TN) | 1 (FP) |
| **Actual: Defective** | 37 (FN) | 47 (TP) |

### toothbrush

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 11 (TN) | 1 (FP) |
| **Actual: Defective** | 20 (FN) | 10 (TP) |

### transistor

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 59 (TN) | 1 (FP) |
| **Actual: Defective** | 29 (FN) | 11 (TP) |

### wood

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 18 (TN) | 1 (FP) |
| **Actual: Defective** | 6 (FN) | 54 (TP) |

### zipper

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 32 (TN) | 0 (FP) |
| **Actual: Defective** | 79 (FN) | 40 (TP) |