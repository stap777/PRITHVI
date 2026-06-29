"""
Climate API Router.

Purpose:
    Exposes endpoints for historical climate data lookup, current metrics, 
    and dashboard overviews. Mounts prediction and simulation sub-routers.
"""

from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Query, status, HTTPException, Depends
from app.schemas import (
    CommonResponse,
    ClimateHistoryResponse,
    ClimateOverviewResponse,
    ClimateParameter,
)
from app.repositories import BaseClimateRepository, ClimateRepository
from app.services import ClimateService
from app.api.prediction import router as prediction_router
from app.api.simulation import router as simulation_router

router = APIRouter()

# Dependency Injection Resolvers
_repo_instance: Optional[BaseClimateRepository] = None


def get_climate_repository() -> BaseClimateRepository:
    """
    Returns a singleton instance of the BaseClimateRepository implementation.
    """
    global _repo_instance
    if _repo_instance is None:
        _repo_instance = ClimateRepository()
    return _repo_instance


def get_climate_service(
    repo: BaseClimateRepository = Depends(get_climate_repository),
) -> ClimateService:
    """
    Dependency resolver for ClimateService.
    """
    return ClimateService(repo)


@router.get(
    "/history",
    response_model=ClimateHistoryResponse,
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
        description="Name of the district (e.g. 'Ratnagiri')"
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
    service: ClimateService = Depends(get_climate_service),
):
    """
    Validates range dates and returns historical climate observations from service layer.
    """
    if start_date > end_date:
        from fastapi.exceptions import RequestValidationError
        raise RequestValidationError(
            errors=[
                {
                    "loc": ["query", "start_date"],
                    "msg": "start_date must be before or equal to end_date",
                    "type": "value_error"
                }
            ]
        )
    return service.get_historical_data(
        state=state,
        district=district,
        start_date=start_date,
        end_date=end_date,
        variables=variables,
    )


@router.get(
    "/current",
    response_model=CommonResponse,
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
        description="Name of the district (e.g. 'Ratnagiri')"
    ),
    variables: List[ClimateParameter] = Query(
        ...,
        description="List of climate parameters to query."
    ),
    service: ClimateService = Depends(get_climate_service),
):
    """
    Retrieves current climate data from the service layer.
    """
    return service.get_current_data(
        state=state,
        district=district,
        variables=variables,
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
        description="Name of the district (e.g. 'Ratnagiri')"
    ),
):
    """
    Retrieves dashboard overview. Returns HTTP 501 (Not Implemented) for Sprint 3.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Dashboard overview aggregation service is not implemented."
    )

# Include sub-routers under the climate hierarchy
router.include_router(prediction_router)
router.include_router(simulation_router)
