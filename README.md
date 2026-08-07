# Industrial Defect Detection & Maintenance Recommendation System

An end-to-end AI system that simulates automated visual inspection in a
manufacturing environment. Detects product defects, localizes them via
anomaly heatmaps, estimates severity, generates maintenance recommendations,
stores inspection history, visualizes results on a dashboard, and generates
downloadable PDF inspection reports.

Supports **all 15 MVTec AD categories**, with per-category calibrated
detection models and severity thresholds. Backed by a full automated test
suite and a rigorous evaluation pipeline (AUROC, confusion matrix,
precision/recall/F1, pixel-level localization).

---

## Tech Stack

- **AI/ML:** PyTorch, Torchvision, OpenCV, WideResNet50-2 (pretrained feature extractor), PatchCore (anomaly detection), scikit-learn (evaluation metrics)
- **Backend:** FastAPI, SQLAlchemy, Alembic, ReportLab
- **Frontend:** React (Vite), Tailwind CSS, React Router
- **Database:** PostgreSQL
- **Testing:** pytest, httpx (FastAPI TestClient integration tests)

---

## Project Status

✅ Working end-to-end:
- Image upload → category-specific AI inference → anomaly heatmap
- **All 15 MVTec AD categories supported**, each with its own PatchCore memory bank
- Severity estimation — bottle uses manually-reviewed thresholds (Phase 8); all other categories use automated percentile-based calibration (see `docs/calibration_notes_all_categories.md`)
- Rule-based maintenance recommendations
- Results persisted to PostgreSQL, with category tracked per inspection
- **Dashboard** — aggregate statistics across all inspections
- **Inspection History page** — full, browsable table of every past inspection
- **Downloadable PDF inspection reports**
- **Automated test suite** — 26 pytest tests, including category-aware threshold tests
- **Full evaluation suite** — AUROC, precision/recall/F1, confusion matrices, and pixel-level localization AUROC computed across all 15 categories (see `docs/evaluation_report.md`)

🚧 In progress / planned:
- Frontend visual polish
- Basic security hardening (auth, upload limits, rate limiting)
- Deployment

---

## Dataset

This project uses the [MVTec AD dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad)
(registration required). Place each category folder at:

```
dataset/mvtec_ad/<category>/
```

Supported categories: `bottle`, `cable`, `capsule`, `carpet`, `grid`,
`hazelnut`, `leather`, `metal_nut`, `pill`, `screw`, `tile`, `toothbrush`,
`transistor`, `wood`, `zipper`.

Expected structure per category:
```
dataset/mvtec_ad/<category>/
├── train/good/
├── test/{good, <defect_types>}/
└── ground_truth/{<defect_types>}/
```

The system works with a partial set of categories too — `get_available_categories()` only loads what's actually present on disk, so you don't need all 15 downloaded to run the app.

---

## Setup

### 1. Backend

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows Git Bash: source .venv/Scripts/activate
pip install -r backend/requirements.txt
```

Create `backend/.env`:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/defect_detection
```

### 2. Database

```bash
psql -U postgres -h localhost -c "CREATE DATABASE defect_detection;"
cd backend
alembic upgrade head
```

### 3. Build memory banks

Build a memory bank for every available category:
```bash
PYTHONPATH=backend python backend/scripts/build_all_memory_banks.py
```

Or build/rebuild a single category with a custom subsample ratio:
```bash
PYTHONPATH=backend python backend/scripts/build_memory_bank_for_category.py <category> <ratio>
```

### 4. Calibrate severity thresholds

```bash
PYTHONPATH=backend python backend/scripts/calibrate_all_categories.py
```

Or recalibrate specific categories only:
```bash
PYTHONPATH=backend python backend/scripts/calibrate_all_categories.py <category1> <category2>
```

Note: `bottle` always uses its original Phase 8 manually-reviewed thresholds regardless of what this script computes — see `severity_estimator.py`.

### 5. Run the backend

```bash
PYTHONPATH=backend uvicorn main:app --reload --app-dir backend
```

Runs at `http://127.0.0.1:8000`. Interactive API docs at `/docs`. Startup logs show which categories' models loaded successfully.

### 6. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`. The Inspect page includes a category dropdown populated from whichever categories are actually loaded.

### 7. Run the test suite

```bash
cd backend
pytest -v
pytest -v -m "not slow"    # fast pass, skips model-loading tests
```

### 8. Run the evaluation suite

```bash
PYTHONPATH=backend python backend/scripts/evaluate_all_categories.py
```

Outputs `docs/evaluation_results.json` (raw) and `docs/evaluation_report.md` (human-readable, with confusion matrices).

---

## Application Pages

- **Inspect** (`/`) — select a category, upload an image, view anomaly score, severity, heatmap, recommendations, and download a PDF report
- **Dashboard** (`/dashboard`) — aggregate stats across all categories
- **History** (`/history`) — full table of every past inspection with per-row PDF report download

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/categories` | List categories with a currently loaded model |
| POST | `/inspect` | Upload an image + category, run full inspection pipeline |
| GET | `/inspections` | List all past inspections |
| GET | `/dashboard` | Aggregate statistics, recent inspections, score trend |
| GET | `/inspections/{id}/report` | Generate and download a PDF report for one inspection |

Full interactive docs available at `http://127.0.0.1:8000/docs` once the backend is running.

---

## Evaluation Results (Summary)

Full results across all 15 categories are in `docs/evaluation_report.md`. Headline findings:

- **Structural-defect categories perform near-perfectly**: bottle, leather, hazelnut, carpet, metal_nut, and wood all achieve AUROC ≥ 0.98 and recall ≥ 0.90.
- **Subtle textural/print-defect categories are harder**: capsule, screw, toothbrush, and grid show lower AUROC (0.76–0.93) — consistent with published PatchCore benchmarks, where these categories are known to be more difficult.
- **A real calibration bug was found and fixed during evaluation**: the initial automated threshold script used the raw maximum good-image score as the "no defect" ceiling, which was highly sensitive to single outlier images and caused severe recall collapse in several categories (e.g. capsule recall was 0.009 before the fix). Switching to a 95th-percentile-based ceiling substantially recovered recall system-wide with no meaningful loss in precision. See `docs/evaluation_report.md` for before/after detail.
- **A targeted memory-bank-richness experiment produced mixed results**: increasing the subsample ratio (0.1→0.25) for the four weakest categories helped capsule substantially, was neutral for toothbrush, and actually made grid and screw's recall worse — evidence that "more reference data" isn't a universal fix and that texture-heavy, self-similar categories can be hurt by an overly broad definition of "normal." Documented in `docs/evaluation_report.md`.

---

## Project Structure

```
anamoly_detection/
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI routes: inspection, history, dashboard, reports, categories
│   │   ├── core/                # config, categories registry, severity_thresholds.json
│   │   ├── preprocessing/       # image transforms, dataset loader, dataloader
│   │   ├── feature_extraction/  # WideResNet50-2 wrapper
│   │   ├── anomaly_detection/   # patch aggregation, memory bank, PatchCore, inference, heatmaps
│   │   ├── severity/            # per-category calibrated severity estimation
│   │   ├── recommendation/      # rule-based recommendation engine
│   │   ├── reports/             # PDF report generation (ReportLab)
│   │   ├── evaluation/          # AUROC/precision/recall/F1/pixel-level metrics
│   │   ├── db/                  # SQLAlchemy models, session, repository
│   │   └── utils/
│   ├── scripts/                 # build_all_memory_banks, build_memory_bank_for_category,
│   │                             #   calibrate_all_categories, evaluate_all_categories
│   ├── alembic/                 # database migrations
│   ├── tests/                   # pytest test suite (26 tests) + conftest.py fixtures
│   ├── pytest.ini
│   └── main.py
│
├── frontend/                    # React + Vite + Tailwind + React Router
│   └── src/
│       ├── api/                 # backend API client functions
│       ├── components/          # ImageUpload (with category dropdown), InspectionResults
│       └── pages/               # Dashboard, History
│
├── models/                      # trained PatchCore memory banks, one per category (gitignored)
├── dataset/                     # MVTec AD data, all categories (gitignored)
├── reports/                     # generated heatmaps, uploads, PDF reports (gitignored)
├── docs/
│   ├── architecture.md
│   ├── calibration_notes.md                  # bottle's original manual calibration (Phase 8)
│   ├── calibration_notes_all_categories.md   # automated calibration, all categories
│   ├── evaluation_results.json               # raw evaluation metrics
│   └── evaluation_report.md                  # human-readable evaluation report
└── README.md
```

---

## Known Limitations

- Currently, only `bottle`'s severity thresholds were manually reviewed and discussed in depth; all other categories use automated percentile-based calibration, which is faster to scale but less individually scrutinized.
- Some categories (capsule, screw, toothbrush, grid) have meaningfully lower detection performance than others — a genuine model/data limitation for subtle, textural defects, not a bug. Documented with real before/after evidence in `docs/evaluation_report.md`.
- The memory-bank-richness experiment intentionally left grid and screw with slightly worse recall than their original 0.1-subsample versions — a deliberate trade-off favoring capsule's larger gain, documented rather than silently accepted.
- Pixel-level AUROC uses a per-image-averaged approximation, not the exact pooled-pixel method used in the original PatchCore paper — numbers are informative but not directly comparable to published benchmarks.
- PatchCore's memory bank uses random subsampling rather than greedy coreset selection.
- Integration tests run against the real `defect_detection` database rather than an isolated test database.
- No authentication, upload size limits, or rate limiting yet — required before any public deployment.
- PDF reports are regenerated on every request rather than cached.