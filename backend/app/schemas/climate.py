"""
Climate-related schemas for the PRITHVI backend API.

Purpose:
    Defines response structures for historical climate data and dashboard overview summaries.
"""

from datetime import date
from typing import Any, Dict, List, Literal
from pydantic import BaseModel, Field


class ClimateHistoryResponse(BaseModel):
    """
    Standardized payload for successful climate history queries.
    """
    status: Literal["success"] = Field(
        default="success",
        description="Always 'success' for successful responses."
    )
    message: str = Field(
        ...,
        description="Detailed description of the operation result."
    )
    state: str = Field(
        ...,
        description="Indian State name queried."
    )
    district: str = Field(
        ...,
        description="District name queried."
    )
    start_date: date = Field(
        ...,
        description="Start date of the retrieved historical records."
    )
    end_date: date = Field(
        ...,
        description="End date of the retrieved historical records."
    )
    data: List[Dict[str, Any]] = Field(
        ...,
        description="Time-series data points. Each element represents a record on a specific date (e.g. {'date': '2023-01-01', 'Temperature': 24.5, 'Rainfall': 12.0})."
    )


class ClimateOverviewResponse(BaseModel):
    """
    Dashboard overview response containing current status, highlights, and summaries for a district.
    """
    status: Literal["success"] = Field(
        default="success",
        description="Always 'success' for successful responses."
    )
    message: str = Field(
        ...,
        description="Detailed description of the operation result."
    )
    state: str = Field(
        ...,
        description="Indian State name."
    )
    district: str = Field(
        ...,
        description="District name."
    )
    metrics: Dict[str, Any] = Field(
        ...,
        description="Latest recorded metrics for parameters (e.g., {'Temperature': {'value': 28.4, 'unit': '°C'}, 'Rainfall': {'value': 150.0, 'unit': 'mm'}})."
    )
    recent_anomalies: List[Dict[str, Any]] = Field(
        ...,
        description="List of detected anomalies or alerts in the last 30 days."
    )
    forecast_summary: Dict[str, Any] = Field(
        ...,
        description="High-level outlook summary (e.g. next 7 days risk levels, predominant weather prediction)."
    )
