"""
Climate API Router.

Purpose:
    Exposes endpoints for historical climate data lookup, current metrics, 
    and dashboard overviews. Mounts prediction and simulation sub-routers.
"""

from datetime import date
from typing import List
from fastapi import APIRouter, Query, status, HTTPException
from app.schemas import (
    CommonResponse,
    ClimateHistoryResponse,
    ClimateOverviewResponse,
    ClimateParameter,
)
from app.api.prediction import router as prediction_router
from app.api.simulation import router as simulation_router

router = APIRouter()


@router.get(
    "/history",
    response_model=ClimateHistoryResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Get Historical Climate Data",
    description="Retrieves a history timeline of selected climate parameters for an Indian State and district.",
)
async def get_history(
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
    start_date: date = Query(
        ...,
        description="Start date of the historical query range (YYYY-MM-DD)"
    ),
    end_date: date = Query(
        ...,
        description="End date of the historical query range (YYYY-MM-DD)"
    ),
    variables: List[ClimateParameter] = Query(
        ...,
        description="List of climate parameters to fetch (e.g., ['Temperature', 'Rainfall'])."
    ),
):
    """
    Validates range dates and returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": ["query", "start_date"],
                    "msg": "start_date must be before or equal to end_date",
                    "type": "value_error"
                }
            ]
        )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Historical dataset access is not implemented."
    )


@router.get(
    "/current",
    response_model=CommonResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Get Current Climate Metrics",
    description="Retrieves near real-time observed parameters for an Indian State and district.",
)
async def get_current(
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
    variables: List[ClimateParameter] = Query(
        ...,
        description="List of climate parameters to query."
    ),
):
    """
    Retrieves current climate data. Returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Live observation sensors data feed integration is not implemented."
    )


@router.get(
    "/overview",
    response_model=ClimateOverviewResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Get District Climate Overview Dashboard",
    description="Provides a lightweight, aggregated summary of current climate indicators, recent anomalies, and forecast status for frontend dashboard display.",
)
async def get_overview(
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
):
    """
    Retrieves dashboard overview. Returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Dashboard overview aggregation service is not implemented."
    )

# Include sub-routers under the climate hierarchy
router.include_router(prediction_router)
router.include_router(simulation_router)
