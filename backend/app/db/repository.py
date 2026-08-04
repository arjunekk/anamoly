"""
Database operations for Inspection records.

Routes never write raw SQLAlchemy queries directly — they call functions
from this module. This keeps all database access logic in one place and
makes routes easier to read and test.
"""

from sqlalchemy.orm import Session
from app.db.models import Inspection


def create_inspection(
    db: Session,
    product_category: str,
    image_path: str,
    heatmap_path: str,
    anomaly_score: float,
    severity: str,
    recommendations: list[str],
) -> Inspection:
    """Saves a new inspection record and returns it (with id/timestamp populated)."""
    inspection = Inspection(
        product_category=product_category,
        image_path=image_path,
        heatmap_path=heatmap_path,
        anomaly_score=anomaly_score,
        severity=severity,
        recommendation="; ".join(recommendations),
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)  # populates id and server-generated timestamp
    return inspection


def get_all_inspections(db: Session) -> list[Inspection]:
    """Returns all inspections, most recent first — used by Dashboard/History."""
    return db.query(Inspection).order_by(Inspection.timestamp.desc()).all()