# Industrial Defect Detection & Maintenance Recommendation System

An end-to-end AI system that simulates automated visual inspection in a
manufacturing environment. Detects product defects, localizes them via
anomaly heatmaps, estimates severity, generates maintenance recommendations,
stores inspection history, and visualizes results on a dashboard.

Built as a modular, phase-by-phase project — currently supports the
**bottle** category from the MVTec AD dataset.

---

## Tech Stack

- **AI/ML:** PyTorch, Torchvision, OpenCV, WideResNet50-2 (pretrained feature extractor), PatchCore (anomaly detection)
- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Frontend:** React (Vite), Tailwind CSS, React Router
- **Database:** PostgreSQL
- **Reports:** ReportLab (PDF generation)

---

## Project Status

✅ Working end-to-end:
- Image upload → AI inference → anomaly heatmap
- Severity estimation (calibrated against real MVTec test data — see `docs/calibration_notes.md`)
- Rule-based maintenance recommendations
- Results persisted to PostgreSQL
- Dashboard with aggregate statistics (defect rate, severity distribution, score trends, recent inspections)
- Downloadable PDF inspection reports

🚧 In progress:
- Dedicated Inspection History page
- Automated testing (pytest)
- Deployment

---

## Dataset

This project uses the [MVTec AD dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad).
Download it separately (registration required) and place the `bottle/`
category folder at:
dataset/mvtec_ad/bottle/

dataset/mvtec_ad/bottle/
├── train/good/
├── test/{good, broken_large, broken_small, contamination}/
└── ground_truth/{broken_large, broken_small, contamination}/

---

## Setup

### 1. Backend

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows Git Bash: source .venv/Scripts/activate
pip install -r backend/requirements.txt
```

Create `backend/.env`:

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/defect_detection

### 2. Database

Requires PostgreSQL installed and running locally.

```bash
psql -U postgres -h localhost -c "CREATE DATABASE defect_detection;"
cd backend
alembic upgrade head
```

### 3. Build the PatchCore memory bank

The trained memory bank (`models/bottle_memory_bank.pt`) must exist before
running the API. Build it by running:

```bash
PYTHONPATH=backend python backend/tests/test_patchcore.py
```

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

---

## Project Structure
<details>
<summary><strong>📁 Project Structure</strong></summary>

```text
anamoly_detection/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── preprocessing/
│   │   ├── feature_extraction/
│   │   ├── anomaly_detection/
│   │   ├── severity/
│   │   ├── recommendation/
│   │   ├── reports/
│   │   ├── db/
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   └── main.py
├── frontend/
│   └── src/
│       ├── api/
│       ├── components/
│       └── pages/
├── models/
├── dataset/
├── reports/
├── docs/
│   ├── architecture.md
│   └── calibration_notes.md
└── README.md
```

</details>
---

## Known Limitations

- Severity thresholds were calibrated on the bottle category only (83 test
  images). Subtle contamination defects can occasionally be misclassified
  as "no defect" — see `docs/calibration_notes.md` for details and the
  reasoning behind not "fixing" this by overfitting thresholds to one case.
- Currently supports only the `bottle` category; multi-category support
  would require per-category memory banks and recalibrated thresholds.
- PatchCore's memory bank uses random subsampling rather than the paper's
  greedy coreset selection — a deliberate simplicity trade-off (see
  `backend/app/anomaly_detection/memory_bank.py` docstring).

