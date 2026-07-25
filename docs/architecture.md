# Architecture Overview

## Purpose
This document describes the modular architecture of the Industrial Defect
Detection & Maintenance Recommendation System.

## Pipeline
Image → Preprocessing → Feature Extraction (WideResNet50-2) →
Anomaly Detection (PatchCore) → Severity Estimation →
Recommendation Engine → Report Generation → Database → Dashboard

## Module Responsibilities

| Module              | Responsibility                                      |
|---------------------|------------------------------------------------------|
| preprocessing       | Resize, normalize, and prepare images for the model  |
| feature_extraction  | Extract embeddings using pretrained WideResNet50-2   |
| anomaly_detection    | Run PatchCore to compute anomaly score + heatmap     |
| severity            | Convert anomaly score/area into a severity label     |
| recommendation      | Rule-based mapping from severity to maintenance steps|
| reports             | Generate downloadable PDF inspection reports         |
| db                  | Persist inspection records to PostgreSQL             |
| api                 | Expose all of the above via FastAPI endpoints        |

## Design Principles
- Each module has a single, well-defined responsibility.
- The recommendation engine is rule-based now, but designed to be
  swapped for an ML/LLM-based engine later without touching other modules.
- Dataset and model artifacts are excluded from version control.