"""
Schemas Package.

Purpose:
    Exposes Pydantic schemas and enums defining the backend API contracts.
"""

from app.schemas.enums import ClimateParameter
from app.schemas.common import CommonResponse, ErrorResponse
from app.schemas.climate import ClimateHistoryResponse, ClimateOverviewResponse
from app.schemas.prediction import PredictionResponse
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.schemas.metadata import MetadataResponse

__all__ = [
    "ClimateParameter",
    "CommonResponse",
    "ErrorResponse",
    "ClimateHistoryResponse",
    "ClimateOverviewResponse",
    "PredictionResponse",
    "SimulationRequest",
    "SimulationResponse",
    "MetadataResponse",
]
