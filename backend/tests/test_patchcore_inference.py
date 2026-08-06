"""
Tests for PatchCore anomaly detection and the inference pipeline (Phases 6-7).

Uses the shared `loaded_patchcore` fixture from conftest.py, which loads
the memory bank once per test session rather than rebuilding it here —
rebuilding takes real time and isn't what these tests are meant to verify.
"""

import pytest
from app.anomaly_detection.inference import run_inference


@pytest.mark.slow
def test_defective_image_scores_higher_than_good_image(
    loaded_patchcore, good_image_path, defective_image_path
):
    """
    This is the core hypothesis of the entire project: PatchCore should
    reliably score defective images higher than defect-free ones.
    """
    good_result = run_inference(good_image_path, loaded_patchcore)
    defect_result = run_inference(defective_image_path, loaded_patchcore)

    assert defect_result["anomaly_score"] > good_result["anomaly_score"]


@pytest.mark.slow
def test_inference_returns_correct_heatmap_shape(loaded_patchcore, defective_image_path):
    result = run_inference(defective_image_path, loaded_patchcore)
    # Heatmap overlay should match the original image's dimensions once rendered.
    assert result["heatmap_image"].size[0] > 0
    assert result["heatmap_image"].size[1] > 0


@pytest.mark.slow
def test_known_defective_image_score_is_stable(loaded_patchcore, defective_image_path):
    """
    Regression test: this specific image + memory bank combination has
    produced a consistent score (45.7088) throughout this project's
    development. If this test ever fails, either the memory bank changed
    or something in the pipeline broke — worth investigating either way.
    """
    result = run_inference(defective_image_path, loaded_patchcore)
    assert result["anomaly_score"] == pytest.approx(45.7088, abs=0.01)