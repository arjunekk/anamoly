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

from datetime import datetime


class InspectionHistoryItem(BaseModel):
    id: int
    product_category: str
    anomaly_score: float
    severity: str
    recommendation: str
    heatmap_url: str
    timestamp: datetime


class CategoryStat(BaseModel):
    count: int
    average_score: float


class DashboardStats(BaseModel):
    total_inspections: int
    defect_rate: float
    average_anomaly_score: float
    severity_distribution: dict[str, int]
    category_stats: dict[str, CategoryStat]


class TrendPoint(BaseModel):
    timestamp: datetime
    anomaly_score: float


class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_inspections: list[InspectionHistoryItem]
    score_trend: list[TrendPoint]

class InspectionResult(BaseModel):
    id: int
    anomaly_score: float
    severity: str
    recommendations: list[str]
    heatmap_url: str