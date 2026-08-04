"""
API route for retrieving inspection history.

Separated from inspection_routes.py since this route only reads data
(no AI pipeline involved) — a different responsibility deserves its
own file, per the project's modular structure.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repository import get_all_inspections
from app.api.schemas import InspectionHistoryItem

router = APIRouter()


@router.get("/inspections", response_model=list[InspectionHistoryItem])
def list_inspections(db: Session = Depends(get_db)):
    """Returns all past inspections, most recent first."""
    inspections = get_all_inspections(db)

    return [
        InspectionHistoryItem(
            id=insp.id,
            product_category=insp.product_category,
            anomaly_score=insp.anomaly_score,
            severity=insp.severity,
            recommendation=insp.recommendation,
            heatmap_url=f"/static/heatmaps/{insp.heatmap_path.split('/')[-1].split(chr(92))[-1]}",
            timestamp=insp.timestamp,
        )
        for insp in inspections
    ]