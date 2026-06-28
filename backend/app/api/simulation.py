"""
Simulation API Router.

Purpose:
    Defines the contract for launching disaster or climate anomaly simulations.
"""

from fastapi import APIRouter, Body, status, HTTPException
from app.schemas import SimulationRequest, SimulationResponse

router = APIRouter()


@router.post(
    "/simulate",
    response_model=SimulationResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Trigger Scenario Simulation",
    description="Initiates a digital twin climate simulation run based on custom anomaly settings and returns tracking and metrics.",
)
async def run_simulation(
    payload: SimulationRequest = Body(
        ...,
        description="Parameters defining the simulation scenario type, location, intensity, and duration."
    )
):
    """
    Triggers simulation and returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Digital twin simulation engine is not implemented."
    )
