"""
ML Prediction Layer Test Suite.

This module asserts the execution behavior of the ML service layer, 
including normal pipeline inference runs and exception guards.

TODO:
    * Mock model weight loading steps to avoid disk operations.
"""

import pytest

from app.services.prediction_service import PredictionService
from app.schemas.prediction import PredictionRequest
from app.exceptions.handlers import ModelLoadError


def test_prediction_service_success():
    """Verifies that normal service prediction execution runs fine."""
    service = PredictionService()
    request = PredictionRequest(
        latitude=21.0,
        longitude=76.0,
        target_metric="precipitation",
        horizon_months=12,
        model_name="convlstm_ensemble"
    )
    
    response = service.predict_metric(request)
    assert response.latitude == 21.0
    assert response.target_metric == "precipitation"
    assert len(response.predictions) == 12
    assert response.predictions[0].predicted_value > 0.0


def test_prediction_service_model_load_failure():
    """Verifies that requesting an invalid model raises a load exception."""
    service = PredictionService()
    # Force model load error via unrecognized target name
    request = PredictionRequest(
        latitude=21.0,
        longitude=76.0,
        target_metric="precipitation",
        horizon_months=6,
        model_name="invalid_model_checkpoint"
    )
    
    with pytest.raises(ModelLoadError) as exc_info:
        service.predict_metric(request)
        
    assert "Model weight file signature" in str(exc_info.value)
