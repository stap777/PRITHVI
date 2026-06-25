"""
Digital Twin Simulation Router.

This controller exposes REST API endpoints for launching multi-hazard scenario
runs (SSP paths, severe storms) and inspecting spatial disaster predictions.

Attributes:
    router: Simulation endpoints router instance.

TODO:
    * Connect Celery/Redis task runner to execute long-running GIS simulations.
    * Enable WebSocket endpoints to stream real-time grid updates.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query, status

from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.simulation_service import SimulationService

router = APIRouter()


# Dependency provider for Simulation Service
def get_simulation_service() -> SimulationService:
    """Dependency injection provider for Simulation Service."""
    return SimulationService()


@router.post(
    "/run",
    response_model=SimulationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger Digital Twin Simulation",
    description="Asynchronously launch flood, drought, or agriculture crop stress projections.",
)
async def run_simulation(
    request: SimulationRequest,
    service: SimulationService = Depends(get_simulation_service)
):
    """
    Spawns computational digital twin runs across the selected region.
    """
    return service.execute_simulation(request)


@router.get(
    "/scenarios",
    status_code=status.HTTP_200_OK,
    summary="List Available Climate Pathways",
    description="Retrieve list of supported IPCC SSP emission pathways and historical benchmarks.",
)
async def list_scenarios(
    service: SimulationService = Depends(get_simulation_service)
) -> List[Dict[str, Any]]:
    """
    Exposes supported climate scenarios and pathway files.
    """
    return service.get_scenarios_list()


@router.get(
    "/{simulation_id}",
    response_model=SimulationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Simulation Results",
    description="Poll or fetch final computed metrics for a given simulation session ID.",
)
async def get_simulation_results(
    simulation_id: str,
    service: SimulationService = Depends(get_simulation_service)
):
    """
    Retrieves execution state and outputs for a specific digital twin run session.
    """
    return service.get_simulation_status(simulation_id)
