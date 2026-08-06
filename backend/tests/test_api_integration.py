"""
Integration tests for the FastAPI backend (Phases 9, 11, 12, 13).

Uses FastAPI's TestClient, which runs the app in-process without needing
a live uvicorn server — requests are simulated directly against the app
object. This still hits your REAL database (defect_detection), since we
haven't set up a separate test database — see the note on this trade-off
below the tests.
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFECTIVE_IMAGE = PROJECT_ROOT / "dataset" / "mvtec_ad" / "bottle" / "test" / "broken_large" / "000.png"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.integration
@pytest.mark.slow
def test_inspect_endpoint_returns_expected_fields():
    with open(DEFECTIVE_IMAGE, "rb") as f:
        response = client.post("/inspect", files={"file": ("test.png", f, "image/png")})

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "anomaly_score" in data
    assert "severity" in data
    assert "recommendations" in data
    assert "heatmap_url" in data
    assert isinstance(data["recommendations"], list)


@pytest.mark.integration
def test_inspect_rejects_unsupported_file_type():
    fake_file_content = b"not a real image"
    response = client.post(
        "/inspect", files={"file": ("test.txt", fake_file_content, "text/plain")}
    )
    assert response.status_code == 400


@pytest.mark.integration
def test_inspections_history_returns_a_list():
    response = client.get("/inspections")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.integration
def test_dashboard_returns_expected_structure():
    response = client.get("/dashboard")
    assert response.status_code == 200
    data = response.json()

    assert "stats" in data
    assert "recent_inspections" in data
    assert "score_trend" in data
    assert "total_inspections" in data["stats"]