"""
SQLAlchemy ORM models — Python classes that map directly to database
tables. This file defines the Inspection table exactly matching the
fields specified in the original project spec.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    product_category = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    heatmap_path = Column(String, nullable=False)
    anomaly_score = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())