"""
API route for running a defect inspection on an uploaded image.

This route ties together every module built in Phases 3-8: it saves
the upload, runs the PatchCore inference pipeline, estimates severity,
generates recommendations, saves the result to the database, and
returns a structured response.
"""

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR, HEATMAP_DIR
from app.anomaly_detection.inference import run_inference
from app.severity.severity_estimator import estimate_severity
from app.recommendation.recommendation_engine import get_recommendations
from app.api.schemas import InspectionResult
from app.api.model_state import get_patchcore_model
from app.db.database import get_db
from app.db.repository import create_inspection

router = APIRouter()


@router.post("/inspect", response_model=InspectionResult)
async def inspect_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts an uploaded image, runs the full defect detection pipeline,
    saves the result to the database, and returns the anomaly score,
    severity, recommendations, and a URL to the generated heatmap overlay.
    """
    allowed_extensions = {".png", ".jpg", ".jpeg"}
    file_ext = "." + file.filename.split(".")[-1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Allowed: {allowed_extensions}",
        )

    unique_id = uuid.uuid4().hex
    saved_image_path = UPLOAD_DIR / f"{unique_id}{file_ext}"

    with open(saved_image_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    patchcore = get_patchcore_model()

    result = run_inference(saved_image_path, patchcore)
    severity = estimate_severity(result["anomaly_score"])
    recommendations = get_recommendations(severity)

    heatmap_filename = f"{unique_id}_heatmap.png"
    heatmap_path = HEATMAP_DIR / heatmap_filename
    result["heatmap_image"].save(heatmap_path)

    
    # Persist this inspection to the database.
    saved_inspection = create_inspection(
        db=db,
        product_category="bottle",  # hardcoded for now — only one category supported so far
        image_path=str(saved_image_path),
        heatmap_path=str(heatmap_path),
        anomaly_score=result["anomaly_score"],
        severity=severity.value,
        recommendations=recommendations,
    )

    return InspectionResult(
        id=saved_inspection.id,
        anomaly_score=result["anomaly_score"],
        severity=severity.value,
        recommendations=recommendations,
        heatmap_url=f"/static/heatmaps/{heatmap_filename}",
    )