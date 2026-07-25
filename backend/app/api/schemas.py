"""
Pydantic models defining the shape of API responses.

Purpose: FastAPI uses these to validate outgoing data and auto-generate
API documentation (Swagger UI). Defining this explicitly, rather than
returning raw dicts, means the contract between backend and frontend
is enforced by code, not just assumed.
"""

from pydantic import BaseModel


class InspectionResult(BaseModel):
    anomaly_score: float
    severity: str
    recommendations: list[str]
    heatmap_url: str