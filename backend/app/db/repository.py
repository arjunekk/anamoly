"""
Database operations for Inspection records.

Routes never write raw SQLAlchemy queries directly — they call functions
from this module. This keeps all database access logic in one place and
makes routes easier to read and test.
"""

from sqlalchemy.orm import Session
from app.db.models import Inspection
from sqlalchemy import func

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




def get_dashboard_stats(db: Session) -> dict:
    """
    Computes aggregate statistics across all inspections for the dashboard.
    """
    total_inspections = db.query(func.count(Inspection.id)).scalar() or 0

    if total_inspections == 0:
        return {
            "total_inspections": 0,
            "defect_rate": 0.0,
            "average_anomaly_score": 0.0,
            "severity_distribution": {},
            "category_stats": {},
        }

    # Defect rate: percentage of inspections with severity != "none"
    defective_count = (
        db.query(func.count(Inspection.id))
        .filter(Inspection.severity != "none")
        .scalar()
        or 0
    )
    defect_rate = round((defective_count / total_inspections) * 100, 2)

    average_score = db.query(func.avg(Inspection.anomaly_score)).scalar() or 0.0

    # Severity distribution: count per severity label
    severity_rows = (
        db.query(Inspection.severity, func.count(Inspection.id))
        .group_by(Inspection.severity)
        .all()
    )
    severity_distribution = {severity: count for severity, count in severity_rows}

    # Category-wise stats: count and average score per product category
    category_rows = (
        db.query(
            Inspection.product_category,
            func.count(Inspection.id),
            func.avg(Inspection.anomaly_score),
        )
        .group_by(Inspection.product_category)
        .all()
    )
    category_stats = {
        category: {"count": count, "average_score": round(float(avg_score), 2)}
        for category, count, avg_score in category_rows
    }

    return {
        "total_inspections": total_inspections,
        "defect_rate": defect_rate,
        "average_anomaly_score": round(float(average_score), 2),
        "severity_distribution": severity_distribution,
        "category_stats": category_stats,
    }


def get_recent_inspections(db: Session, limit: int = 5) -> list[Inspection]:
    """Returns the N most recent inspections, for the dashboard's 'recent activity' view."""
    return (
        db.query(Inspection)
        .order_by(Inspection.timestamp.desc())
        .limit(limit)
        .all()
    )


def get_score_trend(db: Session, limit: int = 20) -> list[dict]:
    """
    Returns the last N inspections' scores in chronological order (oldest first),
    for plotting a trend line over time.
    """
    rows = (
        db.query(Inspection.timestamp, Inspection.anomaly_score)
        .order_by(Inspection.timestamp.desc())
        .limit(limit)
        .all()
    )
    # Reverse so the trend chart reads left-to-right, oldest to newest.
    rows.reverse()
    return [{"timestamp": ts, "anomaly_score": score} for ts, score in rows]