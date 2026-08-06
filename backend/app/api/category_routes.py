"""
Route for the frontend to discover which categories currently have a
loaded model available — used to populate the upload page's category
dropdown, so it only ever offers categories that will actually work.
"""

from fastapi import APIRouter
from app.api.model_state import get_loaded_categories

router = APIRouter()


@router.get("/categories")
def list_categories():
    return {"categories": get_loaded_categories()}