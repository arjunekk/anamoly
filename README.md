# Industrial Defect Detection & Maintenance Recommendation System

An end-to-end AI system that simulates automated visual inspection in a
manufacturing environment. Detects product defects, localizes them via
anomaly heatmaps, estimates severity, and generates maintenance
recommendations.

## Tech Stack
- **AI/ML:** PyTorch, Torchvision, OpenCV, WideResNet50-2, PatchCore
- **Backend:** FastAPI
- **Frontend:** React + Tailwind CSS
- **Database:** PostgreSQL

## Dataset
This project uses the [MVTec AD dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad).
Download it separately and place the `bottle/` category under `dataset/mvtec_ad/`.

## Project Status
🚧 In development — see `docs/architecture.md` for design details.

## Setup
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
\`\`\`