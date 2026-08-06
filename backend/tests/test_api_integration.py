"""
Integration tests for the FastAPI backend (Phases 9, 11, 12, 13).

Uses FastAPI's TestClient inside a `with` block, which properly triggers
the app's lifespan startup/shutdown events (including loading the
PatchCore model) — using TestClient without `with` skips lifespan
entirely, which is why the model must be loaded via this fixture.
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from main import app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFECTIVE_IMAGE = PROJECT_ROOT / "dataset" / "mvtec_ad" / "bottle" / "test" / "broken_large" / "000.png"


@pytest.fixture(scope="module")
def client():
    """
    Yields a TestClient with lifespan events triggered — this is what
    actually calls load_patchcore_model() at "startup" before any test runs.
    scope="module" means this setup happens once for all tests in this
    file, not once per test.
    """
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.integration
@pytest.mark.slow
def test_inspect_endpoint_returns_expected_fields(client):
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
def test_inspect_rejects_unsupported_file_type(client):
    fake_file_content = b"not a real image"
    response = client.post(
        "/inspect", files={"file": ("test.txt", fake_file_content, "text/plain")}
    )
    assert response.status_code == 400


@pytest.mark.integration
def test_inspections_history_returns_a_list(client):
    response = client.get("/inspections")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.integration
def test_dashboard_returns_expected_structure(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
    data = response.json()

    assert "stats" in data
    assert "recent_inspections" in data
    assert "score_trend" in data
    assert "total_inspections" in data["stats"]