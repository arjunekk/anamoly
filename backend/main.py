"""
Entry point for the FastAPI backend.
This is intentionally minimal in Phase 1 — real routes are added in Phase 9.
"""

from fastapi import FastAPI

app = FastAPI(title="Industrial Defect Detection API")


@app.get("/health")
def health_check():
    """Basic endpoint to confirm the server is running."""
    return {"status": "ok"}