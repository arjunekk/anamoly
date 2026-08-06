# Industrial Defect Detection & Maintenance Recommendation System

An end-to-end AI system that simulates automated visual inspection in a
manufacturing environment. Detects product defects, localizes them via
anomaly heatmaps, estimates severity, generates maintenance recommendations,
stores inspection history, visualizes results on a dashboard, and generates
downloadable PDF inspection reports.

Built as a modular, phase-by-phase project — currently supports the
**bottle** category from the MVTec AD dataset. Backed by a full automated
test suite (23 tests, `pytest`).

---

## Tech Stack

- **AI/ML:** PyTorch, Torchvision, OpenCV, WideResNet50-2 (pretrained feature extractor), PatchCore (anomaly detection)
- **Backend:** FastAPI, SQLAlchemy, Alembic, ReportLab
- **Frontend:** React (Vite), Tailwind CSS, React Router
- **Database:** PostgreSQL
- **Testing:** pytest, httpx (FastAPI TestClient integration tests)

---

## Project Status

✅ Working end-to-end:
- Image upload → AI inference → anomaly heatmap
- Severity estimation (calibrated against real MVTec test data — see `docs/calibration_notes.md`)
- Rule-based maintenance recommendations
- Results persisted to PostgreSQL
- **Dashboard** — aggregate statistics (defect rate, severity distribution, score trends, recent inspections)
- **Inspection History page** — full, browsable table of every past inspection
- **Downloadable PDF inspection reports** — generated on-demand, linked from both the Inspect and History pages
- **Automated test suite** — 23 pytest tests covering data pipeline, feature extraction, PatchCore, severity/recommendation logic, and full API integration

🚧 In progress / planned:
- Multi-category support (currently bottle only)
- Formal evaluation (AUROC, confusion matrix, precision/recall/F1, pixel-level localization accuracy against ground truth masks)
- Frontend visual polish
- Basic security hardening (auth, upload limits, rate limiting) — not yet needed for local development, required before any public deployment
- Deployment

---

## Dataset

This project uses the [MVTec AD dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad).
Download it separately (registration required) and place the `bottle/`
category folder at:

```
dataset/mvtec_ad/bottle/
```

Expected structure:
```
dataset/mvtec_ad/bottle/
├── train/good/
├── test/{good, broken_large, broken_small, contamination}/
└── ground_truth/{broken_large, broken_small, contamination}/
```

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

Requires PostgreSQL installed and running locally.

```bash
psql -U postgres -h localhost -c "CREATE DATABASE defect_detection;"
cd backend
alembic upgrade head
```

### 3. Build the PatchCore memory bank

The trained memory bank (`models/bottle_memory_bank.pt`) must exist before
running the API or the test suite's slower tests. If it doesn't exist yet,
build it by fitting PatchCore against the training DataLoader (see
`backend/app/anomaly_detection/patchcore.py`'s `fit()` method).

### 4. Run the backend

```bash
PYTHONPATH=backend uvicorn main:app --reload --app-dir backend
```

Runs at `http://127.0.0.1:8000`. Interactive API docs at `/docs`.

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`.

### 6. Run the test suite

```bash
cd backend
pytest -v
```

Fast pass only (skips model-loading tests):
```bash
pytest -v -m "not slow"
```

---

## Application Pages

- **Inspect** (`/`) — upload an image, view anomaly score, severity, heatmap, recommendations, and download a PDF report
- **Dashboard** (`/dashboard`) — aggregate stats: total inspections, defect rate, severity distribution, average score, recent inspection trend
- **History** (`/history`) — full table of every past inspection with per-row PDF report download

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| POST | `/inspect` | Upload an image, run full inspection pipeline |
| GET | `/inspections` | List all past inspections |
| GET | `/dashboard` | Aggregate statistics, recent inspections, score trend |
| GET | `/inspections/{id}/report` | Generate and download a PDF report for one inspection |

Full interactive docs available at `http://127.0.0.1:8000/docs` once the backend is running.

---

## Testing

23 automated tests across:
- **Data pipeline** — dataset loading, preprocessing, normalization/reversibility
- **Feature extraction** — WideResNet50-2 output shapes
- **PatchCore** — the core anomaly detection hypothesis (defective images score higher than good ones), heatmap generation, a regression test locking in a known-correct score
- **Severity & recommendations** — threshold boundaries, including a test that explicitly documents the known contamination false-negative edge case (see `docs/calibration_notes.md`)
- **API integration** — full FastAPI request/response cycle via `TestClient`, including a rejected-file-type test

Tests are marked `slow` (model-loading) and `integration` (hits the real
database — see Known Limitations) so subsets can be run selectively.

---

## Project Structure

```
anamoly_detection/
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI routes: inspection, history, dashboard, reports
│   │   ├── core/                # config
│   │   ├── preprocessing/       # image transforms, dataset loader, dataloader
│   │   ├── feature_extraction/  # WideResNet50-2 wrapper
│   │   ├── anomaly_detection/   # patch aggregation, memory bank, PatchCore, inference, heatmaps
│   │   ├── severity/            # severity estimation (calibrated thresholds)
│   │   ├── recommendation/      # rule-based recommendation engine
│   │   ├── reports/             # PDF report generation (ReportLab)
│   │   ├── db/                  # SQLAlchemy models, session, repository
│   │   └── utils/
│   ├── alembic/                 # database migrations
│   ├── tests/                   # pytest test suite (23 tests) + conftest.py fixtures
│   ├── pytest.ini
│   └── main.py
│
├── frontend/                    # React + Vite + Tailwind + React Router
│   └── src/
│       ├── api/                 # backend API client functions
│       ├── components/          # ImageUpload, InspectionResults
│       └── pages/               # Dashboard, History
│
├── models/                      # trained PatchCore memory bank (gitignored)
├── dataset/                     # MVTec AD data (gitignored)
├── reports/                     # generated heatmaps, uploads, PDF reports (gitignored)
├── docs/
│   ├── architecture.md
│   └── calibration_notes.md     # severity threshold derivation + known limitations
└── README.md
```

---

## Known Limitations

- Severity thresholds were calibrated on the bottle category only (83 test
  images). Subtle contamination defects can occasionally be misclassified
  as "no defect" — see `docs/calibration_notes.md` for details and the
  reasoning behind not "fixing" this by overfitting thresholds to one case.
  This is also captured as an explicit test case in
  `test_severity_and_recommendations.py`.
- Currently supports only the `bottle` category; multi-category support
  would require per-category memory banks and recalibrated thresholds.
- PatchCore's memory bank uses random subsampling rather than the paper's
  greedy coreset selection — a deliberate simplicity trade-off (see
  `backend/app/anomaly_detection/memory_bank.py` docstring).
- No formal evaluation metrics computed yet (AUROC, precision/recall,
  pixel-level localization against ground truth masks) — planned as a
  dedicated evaluation phase.
- Integration tests in `test_api_integration.py` run against the real
  `defect_detection` database rather than an isolated test database —
  acceptable for a local-development portfolio project, but a genuine
  limitation if this were a production system.
- No authentication, upload size limits, or rate limiting yet — acceptable
  for local development, required before any public deployment.
- PDF reports are regenerated on every request rather than cached.