# Model Evaluation Report

Computed across all available MVTec AD categories. Image-level metrics compare the raw anomaly score (AUROC) and the system's actual severity decision (precision/recall/F1/confusion matrix) against ground truth labels. Pixel-level AUROC measures how well the heatmap localizes the true defect region, averaged per-image across defective test images with a ground truth mask (a lighter-weight approximation of the paper convention of pooling all pixels together — see project documentation for this trade-off).


## Summary Table

| Category | Image AUROC | Precision | Recall | F1 | Pixel AUROC (mean) | Test Images |
|---|---|---|---|---|---|---|
| bottle | 0.995 | 0.939 | 0.984 | 0.961 | 0.987 | 83 |
| cable | 0.852 | 0.943 | 0.543 | 0.690 | 0.960 | 150 |
| capsule | 0.800 | 0.917 | 0.202 | 0.331 | 0.982 | 132 |
| carpet | 0.984 | 0.976 | 0.933 | 0.954 | 0.989 | 117 |
| grid | 0.825 | 0.969 | 0.544 | 0.697 | 0.969 | 78 |
| hazelnut | 0.997 | 0.972 | 1.000 | 0.986 | 0.988 | 110 |
| leather | 1.000 | 0.979 | 1.000 | 0.989 | 0.996 | 124 |
| metal_nut | 0.992 | 0.979 | 0.989 | 0.984 | 0.972 | 115 |
| pill | 0.862 | 0.976 | 0.574 | 0.723 | 0.963 | 167 |
| screw | 0.832 | 0.971 | 0.563 | 0.713 | 0.983 | 160 |
| tile | 0.923 | 0.968 | 0.714 | 0.822 | 0.949 | 117 |
| toothbrush | 0.831 | 0.909 | 0.333 | 0.488 | 0.980 | 42 |
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
| **Actual: Defective** | 87 (FN) | 22 (TP) |

### carpet

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 26 (TN) | 2 (FP) |
| **Actual: Defective** | 6 (FN) | 83 (TP) |

### grid

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 20 (TN) | 1 (FP) |
| **Actual: Defective** | 26 (FN) | 31 (TP) |

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
| **Actual: Good** | 39 (TN) | 2 (FP) |
| **Actual: Defective** | 52 (FN) | 67 (TP) |

### tile

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 31 (TN) | 2 (FP) |
| **Actual: Defective** | 24 (FN) | 60 (TP) |

### toothbrush

| | Predicted: No Defect | Predicted: Defect |
|---|---|---|
| **Actual: Good** | 11 (TN) | 1 (FP) |
| **Actual: Defective** | 20 (FN) | 10 (TP) |

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