"""
API route for dashboard statistics: aggregate stats, recent inspections,
and score trend data — everything the Dashboard frontend page needs in
a single request.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repository import get_dashboard_stats, get_recent_inspections, get_score_trend
from app.api.schemas import DashboardResponse, InspectionHistoryItem

router = APIRouter()


def _heatmap_url_from_path(heatmap_path: str) -> str:
    filename = heatmap_path.split("/")[-1].split("\\")[-1]
    return f"/static/heatmaps/{filename}"


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """Returns everything the dashboard page needs in one request."""
    stats = get_dashboard_stats(db)
    recent = get_recent_inspections(db, limit=5)
    trend = get_score_trend(db, limit=20)

    recent_items = [
        InspectionHistoryItem(
            id=insp.id,
            product_category=insp.product_category,
            anomaly_score=insp.anomaly_score,
            severity=insp.severity,
            recommendation=insp.recommendation,
            heatmap_url=_heatmap_url_from_path(insp.heatmap_path),
            timestamp=insp.timestamp,
        )
        for insp in recent
    ]

    return DashboardResponse(
        stats=stats,
        recent_inspections=recent_items,
        score_trend=trend,
    )