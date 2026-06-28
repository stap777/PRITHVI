"""
Prediction API Router.

Purpose:
    Defines the contract for retrieving forecasting/prediction weather metrics.
"""

from typing import List
from fastapi import APIRouter, Query, status, HTTPException
from app.schemas import PredictionResponse, ClimateParameter

router = APIRouter()


@router.get(
    "/predictions",
    response_model=PredictionResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Retrieve Climate Predictions",
    description="Provides machine learning based climate forecasts for a selected Indian district over a given horizon.",
)
async def get_predictions(
    state: str = Query(
        ...,
        min_length=2,
        description="Name of the Indian State (e.g. 'Maharashtra')"
    ),
    district: str = Query(
        ...,
        min_length=2,
        description="Name of the district (e.g. 'Pune')"
    ),
    horizon_days: int = Query(
        ...,
        ge=1,
        le=365,
        description="Number of days into the future to forecast (1 to 365)"
    ),
    variables: List[ClimateParameter] = Query(
        ...,
        description="List of target climate parameters to predict."
    )
):
    """
    Retrieves forecasted climate values. Returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="ML Prediction service integration is not implemented."
    )
