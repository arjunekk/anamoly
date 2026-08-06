"""
Evaluation metrics for the anomaly detection system.

Computes image-level classification metrics (AUROC, precision, recall,
F1, confusion matrix) and pixel-level localization metrics (per-image
AUROC comparing the predicted heatmap against ground truth defect masks).
"""

import numpy as np
import cv2
from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


def compute_image_level_metrics(y_true, y_scores, y_pred_defective):
    """
    Args:
        y_true: list of 0/1, 1 = actually defective (ground truth)
        y_scores: list of raw anomaly scores (continuous) — used for AUROC
        y_pred_defective: list of 0/1, 1 = system flagged as defective
            (severity != NONE) — used for precision/recall/F1/confusion matrix

    Returns:
        dict of computed metrics
    """
    auroc = roc_auc_score(y_true, y_scores) if len(set(y_true)) > 1 else None

    precision = precision_score(y_true, y_pred_defective, zero_division=0)
    recall = recall_score(y_true, y_pred_defective, zero_division=0)
    f1 = f1_score(y_true, y_pred_defective, zero_division=0)
    cm = confusion_matrix(y_true, y_pred_defective, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    return {
        "auroc": auroc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }


def compute_pixel_level_auroc(heatmap_28x28, mask_path, target_size):
    """
    Upsamples the raw 28x28 patch-distance heatmap to the mask's resolution
    and computes pixel-level AUROC against the ground truth binary mask,
    for one defective image.

    Returns None if the mask couldn't be read, or has only one class
    present (shouldn't normally happen for a real defect mask, but
    guarded defensively rather than letting sklearn raise).
    """
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return None
    mask_binary = (mask > 127).astype(np.uint8)

    heatmap_np = heatmap_28x28.numpy()
    upsampled = cv2.resize(heatmap_np, target_size, interpolation=cv2.INTER_CUBIC)

    mask_flat = mask_binary.flatten()
    heatmap_flat = upsampled.flatten()

    if len(set(mask_flat)) < 2:
        return None

    return roc_auc_score(mask_flat, heatmap_flat)