# Automated Multi-Category Calibration

Thresholds derived automatically via percentile-based splitting of defective test scores per category (33rd/66th percentile), with the 'none' ceiling set to each category's own max good-image score. See conversation history for full reasoning and trade-offs versus the manual approach used for bottle.


## capsule

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| crack | 23 | 28.4 | 51.59 | 37.88 |
| faulty_imprint | 22 | 24.67 | 40.34 | 31.54 |
| good | 23 | 17.4 | 34.67 | 24.78 |
| poke | 21 | 29.05 | 47.68 | 35.99 |
| scratch | 23 | 24.54 | 39.66 | 30.05 |
| squeeze | 20 | 31.22 | 43.54 | 39.42 |

**Thresholds:** None ≤ 32.23 | Minor ≤ 32.24 | Moderate ≤ 37.39 | Critical above


## toothbrush

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| defective | 30 | 30.78 | 53.77 | 44.54 |
| good | 12 | 26.07 | 47.95 | 33.11 |

**Thresholds:** None ≤ 47.55 | Minor ≤ 47.56 | Moderate ≤ 48.25 | Critical above


## screw

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| good | 41 | 25.79 | 42.91 | 29.53 |
| manipulated_front | 24 | 28.22 | 38.39 | 33.56 |
| scratch_head | 24 | 31.11 | 41.42 | 36.28 |
| scratch_neck | 25 | 30.4 | 48.45 | 40.26 |
| thread_side | 23 | 28.5 | 38.22 | 31.12 |
| thread_top | 23 | 29.42 | 41.69 | 33.27 |

**Thresholds:** None ≤ 34.43 | Minor ≤ 34.44 | Moderate ≤ 36.3 | Critical above


## grid

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| bent | 12 | 33.77 | 43.39 | 38.26 |
| broken | 12 | 35.71 | 53.37 | 41.78 |
| glue | 11 | 31.68 | 39.83 | 35.99 |
| good | 21 | 31.6 | 41.49 | 35.17 |
| metal_contamination | 11 | 33.02 | 49.96 | 40.89 |
| thread | 11 | 30.36 | 45.82 | 36.71 |

**Thresholds:** None ≤ 38.6 | Minor ≤ 38.61 | Moderate ≤ 39.79 | Critical above
