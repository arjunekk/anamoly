# Automated Multi-Category Calibration

Thresholds derived automatically via percentile-based splitting of defective test scores per category (33rd/66th percentile), with the 'none' ceiling set to each category's own max good-image score. See conversation history for full reasoning and trade-offs versus the manual approach used for bottle.


## bottle

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| broken_large | 20 | 40.32 | 49.59 | 44.42 |
| broken_small | 22 | 38.76 | 47.05 | 42.93 |
| contamination | 21 | 29.51 | 61.81 | 42.17 |
| good | 20 | 22.69 | 33.26 | 28.48 |

**Thresholds:** None ≤ 33.26 | Minor ≤ 41.48 | Moderate ≤ 44.87 | Critical above


## cable

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| bent_wire | 13 | 41.79 | 56.55 | 51.65 |
| cable_swap | 12 | 35.42 | 40.93 | 37.11 |
| combined | 11 | 40.51 | 58.12 | 46.49 |
| cut_inner_insulation | 14 | 39.2 | 48.65 | 44.63 |
| cut_outer_insulation | 10 | 39.2 | 45.5 | 42.18 |
| good | 58 | 34.18 | 47.95 | 37.69 |
| missing_cable | 12 | 36.31 | 47.74 | 40.73 |
| missing_wire | 10 | 40.31 | 51.03 | 45.11 |
| poke_insulation | 10 | 37.33 | 44.93 | 40.78 |

**Thresholds:** None ≤ 47.95 | Minor ≤ 47.96 | Moderate ≤ 47.97 | Critical above


## capsule

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| crack | 23 | 28.47 | 51.59 | 38.78 |
| faulty_imprint | 22 | 25.62 | 40.06 | 33.29 |
| good | 23 | 19.91 | 49.74 | 28.98 |
| poke | 21 | 29.94 | 49.4 | 37.42 |
| scratch | 23 | 25.43 | 39.66 | 31.29 |
| squeeze | 20 | 31.79 | 44.73 | 40.12 |

**Thresholds:** None ≤ 49.74 | Minor ≤ 49.75 | Moderate ≤ 49.76 | Critical above


## carpet

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| color | 19 | 27.57 | 45.05 | 37.17 |
| cut | 17 | 33.66 | 49.75 | 40.99 |
| good | 28 | 22.74 | 30.23 | 25.86 |
| hole | 17 | 30.81 | 50.92 | 42.92 |
| metal_contamination | 17 | 28.62 | 53.79 | 45.44 |
| thread | 19 | 24.88 | 49.22 | 40.42 |

**Thresholds:** None ≤ 30.23 | Minor ≤ 38.79 | Moderate ≤ 44.26 | Critical above


## grid

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| bent | 12 | 35.64 | 44.33 | 39.76 |
| broken | 12 | 36.62 | 53.54 | 41.93 |
| glue | 11 | 33.89 | 42.66 | 37.67 |
| good | 21 | 32.7 | 42.03 | 36.09 |
| metal_contamination | 11 | 37.05 | 49.5 | 42.16 |
| thread | 11 | 32.73 | 46.53 | 38.53 |

**Thresholds:** None ≤ 42.03 | Minor ≤ 42.04 | Moderate ≤ 42.05 | Critical above


## hazelnut

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| crack | 18 | 39.59 | 47.5 | 43.86 |
| cut | 17 | 40.91 | 52.07 | 46.8 |
| good | 40 | 30.09 | 41.96 | 33.76 |
| hole | 18 | 41.23 | 60.0 | 48.73 |
| print | 17 | 40.86 | 53.75 | 45.72 |

**Thresholds:** None ≤ 41.96 | Minor ≤ 44.29 | Moderate ≤ 47.4 | Critical above


## leather

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| color | 19 | 40.08 | 61.74 | 49.62 |
| cut | 19 | 34.32 | 55.34 | 45.73 |
| fold | 17 | 35.08 | 48.28 | 41.58 |
| glue | 19 | 43.13 | 63.5 | 51.61 |
| good | 32 | 22.96 | 31.62 | 25.89 |
| poke | 18 | 38.43 | 54.28 | 47.88 |

**Thresholds:** None ≤ 31.62 | Minor ≤ 44.51 | Moderate ≤ 50.25 | Critical above


## metal_nut

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| bent | 25 | 38.53 | 49.24 | 43.57 |
| color | 22 | 34.87 | 50.82 | 41.56 |
| flip | 23 | 43.26 | 49.36 | 45.46 |
| good | 22 | 29.59 | 36.18 | 32.19 |
| scratch | 23 | 31.74 | 44.59 | 39.44 |

**Thresholds:** None ≤ 36.18 | Minor ≤ 41.01 | Moderate ≤ 44.54 | Critical above


## pill

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| color | 25 | 29.76 | 45.22 | 38.34 |
| combined | 17 | 30.76 | 51.8 | 40.07 |
| contamination | 21 | 30.72 | 49.36 | 37.14 |
| crack | 26 | 30.09 | 38.65 | 34.03 |
| faulty_imprint | 19 | 30.88 | 36.52 | 33.68 |
| good | 26 | 28.97 | 36.48 | 31.78 |
| pill_type | 9 | 34.42 | 47.95 | 40.62 |
| scratch | 24 | 30.56 | 40.81 | 35.5 |

**Thresholds:** None ≤ 36.48 | Minor ≤ 36.49 | Moderate ≤ 37.85 | Critical above


## screw

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| good | 41 | 28.42 | 43.07 | 32.39 |
| manipulated_front | 24 | 31.58 | 38.37 | 34.82 |
| scratch_head | 24 | 32.03 | 41.3 | 37.55 |
| scratch_neck | 25 | 32.32 | 49.25 | 41.14 |
| thread_side | 23 | 30.02 | 39.2 | 33.05 |
| thread_top | 23 | 30.32 | 42.1 | 34.48 |

**Thresholds:** None ≤ 43.07 | Minor ≤ 43.08 | Moderate ≤ 43.09 | Critical above


## tile

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| crack | 17 | 37.52 | 58.08 | 49.08 |
| glue_strip | 18 | 39.26 | 48.99 | 43.21 |
| good | 33 | 29.39 | 39.81 | 32.04 |
| gray_stroke | 16 | 30.06 | 40.73 | 33.75 |
| oil | 18 | 36.25 | 51.13 | 41.41 |
| rough | 15 | 31.48 | 47.32 | 36.84 |

**Thresholds:** None ≤ 39.81 | Minor ≤ 39.82 | Moderate ≤ 42.88 | Critical above


## toothbrush

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| defective | 30 | 32.55 | 54.38 | 45.37 |
| good | 12 | 31.58 | 49.07 | 36.52 |

**Thresholds:** None ≤ 49.07 | Minor ≤ 49.08 | Moderate ≤ 49.09 | Critical above


## transistor

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| bent_lead | 10 | 40.75 | 51.87 | 45.82 |
| cut_lead | 10 | 41.28 | 47.2 | 43.73 |
| damaged_case | 10 | 37.56 | 45.61 | 41.04 |
| good | 60 | 31.65 | 46.39 | 36.78 |
| misplaced | 10 | 35.66 | 50.62 | 43.83 |

**Thresholds:** None ≤ 46.39 | Minor ≤ 46.4 | Moderate ≤ 46.41 | Critical above


## wood

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| color | 8 | 44.33 | 55.64 | 50.2 |
| combined | 11 | 44.75 | 55.13 | 51.05 |
| good | 19 | 24.71 | 36.0 | 29.24 |
| hole | 10 | 35.9 | 57.2 | 48.77 |
| liquid | 10 | 35.72 | 52.51 | 44.57 |
| scratch | 21 | 28.1 | 51.01 | 41.55 |

**Thresholds:** None ≤ 36.0 | Minor ≤ 43.77 | Moderate ≤ 49.19 | Critical above


## zipper

| Class | Count | Min | Max | Mean |
|---|---|---|---|---|
| broken_teeth | 19 | 24.12 | 44.56 | 32.92 |
| combined | 16 | 27.38 | 50.82 | 38.67 |
| fabric_border | 17 | 30.38 | 56.9 | 45.17 |
| fabric_interior | 16 | 24.56 | 41.27 | 30.51 |
| good | 32 | 18.64 | 35.77 | 24.18 |
| rough | 17 | 26.77 | 41.23 | 32.78 |
| split_teeth | 18 | 26.1 | 41.68 | 31.33 |
| squeezed_teeth | 16 | 21.0 | 36.79 | 29.72 |

**Thresholds:** None ≤ 35.77 | Minor ≤ 35.78 | Moderate ≤ 35.79 | Critical above
