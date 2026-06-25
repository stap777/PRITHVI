"""
AI Prediction Schemas.

This module defines Pydantic validation structures for AI prediction endpoints,
covering input parameter envelopes and output prediction confidence timeseries.

Classes:
    PredictionRequest: Input parameter model for running AI forecasts.
    ForecastObservation: A predicted timestamp value with confidence intervals.
    PredictionResponse: Output structured API payload from the prediction service.

TODO:
    * Support dynamic selection of ML models (ConvLSTM, XGBoost, etc.) in requests.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Parameters representing target location and parameters for ML models."""
    latitude: float = Field(..., ge=6.0, le=36.0, description="Latitude (India bounds)")
    longitude: float = Field(..., ge=68.0, le=98.0, description="Longitude (India bounds)")
    target_metric: str = Field(
        ...,
        description="Target variable: 'precipitation' or 'surface_temperature'"
    )
    horizon_months: int = Field(
        default=12,
        ge=1,
        le=120,
        description="Forecast length in months (maximum 10 years)"
    )
    model_name: Optional[str] = Field(
        default="convlstm_ensemble",
        description="Specific ML model version to target"
    )


class ForecastObservation(BaseModel):
    """Representing a forecasted metric value at a future timestep."""
    timestep_index: int = Field(..., description="Future index relative to query point")
    date_label: str = Field(..., description="Formatted ISO Date string (YYYY-MM)")
    predicted_value: float = Field(..., description="Estimated model value (mean prediction)")
    confidence_lower: float = Field(..., description="Lower confidence limit (95th percentile)")
    confidence_upper: float = Field(..., description="Upper confidence limit (95th percentile)")


class PredictionResponse(BaseModel):
    """Prediction results payload including target settings and metrics."""
    latitude: float
    longitude: float
    target_metric: str
    horizon_months: int
    model_version: str = Field(..., description="Identified ML model weight signature")
    predictions: List[ForecastObservation] = Field(
        default=[],
        description="Chronological forecast points"
    )
