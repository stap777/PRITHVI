"""
Prediction-related schemas for the PRITHVI backend API.

Purpose:
    Defines response structures for climate parameters forecasting and model predictions.
"""

from typing import Any, Dict, List, Literal
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """
    Standardized payload for successful climate prediction/forecast queries.
    """
    status: Literal["success"] = Field(
        default="success",
        description="Always 'success' for successful responses."
    )
    message: str = Field(
        ...,
        description="Detailed description of the prediction status."
    )
    state: str = Field(
        ...,
        description="Indian State name forecasted."
    )
    district: str = Field(
        ...,
        description="District name forecasted."
    )
    horizon_days: int = Field(
        ...,
        description="Forecast range duration in days."
    )
    predictions: List[Dict[str, Any]] = Field(
        ...,
        description="Time-series predicted points containing date and parameter forecasts (e.g. [{'date': '2026-06-29', 'Temperature': {'mean': 28.5, 'upper': 30.1, 'lower': 26.9}}])."
    )
