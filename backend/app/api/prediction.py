"""
AI Climate Prediction Router.

This controller exposes REST API endpoints for invoking Deep Learning climate models
(ConvLSTM/XGBoost) to forecast variables (temperature, precipitation) across India.

Attributes:
    router: Prediction endpoints router instance.

TODO:
    * Set up background tasks to support heavy batch prediction jobs.
    * Implement token validation dependencies.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, status

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter()


# Dependency provider for Prediction Service
def get_prediction_service() -> PredictionService:
    """Dependency injection provider for ML Prediction Service."""
    return PredictionService()


@router.post(
    "/forecast",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Climate Forecasts",
    description="Run ML model inference to predict temperature or precipitation anomalies.",
)
async def generate_forecast(
    request: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service)
):
    """
    Executes deep learning inference to forecast meteorological attributes.
    """
    return service.predict_metric(request)


@router.get(
    "/models",
    status_code=status.HTTP_200_OK,
    summary="List Warmed Models",
    description="Get metadata of all deep learning model states active in memory.",
)
async def list_models(
    service: PredictionService = Depends(get_prediction_service)
) -> Dict[str, Any]:
    """
    Retrieves system list of loaded model names, targets, and checkpoints.
    """
    return service.get_available_models()
