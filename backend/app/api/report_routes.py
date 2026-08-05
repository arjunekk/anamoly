"""
API route for generating and downloading a PDF report for a single
inspection. Generated on-demand from data already in the database,
rather than pre-generated and stored at inspection time.
"""

from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repository import get_inspection_by_id
from app.reports.report_generator import generate_inspection_report
from app.core.config import PROJECT_ROOT

router = APIRouter()

REPORTS_DIR = PROJECT_ROOT / "reports" / "generated"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/inspections/{inspection_id}/report")
def get_inspection_report(inspection_id: int, db: Session = Depends(get_db)):
    """Generates (or regenerates) and returns a PDF report for one inspection."""
    inspection = get_inspection_by_id(db, inspection_id)

    if inspection is None:
        raise HTTPException(status_code=404, detail=f"Inspection {inspection_id} not found")

    output_path = REPORTS_DIR / f"inspection_{inspection_id}_report.pdf"
    generate_inspection_report(inspection, output_path)

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=f"inspection_{inspection_id}_report.pdf",
    )