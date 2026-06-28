"""
Simulation-related schemas for the PRITHVI backend API.

Purpose:
    Defines request structures (POST body) and response models for climate and disaster simulation runs.
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    """
    Validation contract for triggering a climate/disaster scenario simulation.
    """
    scenario_type: Literal["extreme_rainfall", "drought", "heatwave", "cloudburst"] = Field(
        ...,
        description="Type of weather anomaly or disaster scenario to simulate."
    )
    state: str = Field(
        ...,
        min_length=2,
        description="Indian State containing the target region."
    )
    district: str = Field(
        ...,
        min_length=2,
        description="Target district within the selected State."
    )
    intensity_multiplier: float = Field(
        ...,
        gt=0.0,
        le=5.0,
        description="Scaling factor for the scenario intensity (e.g., 1.5 indicates a 50% increase above normal values)."
    )
    duration_days: int = Field(
        ...,
        ge=1,
        le=90,
        description="Length of the simulation window in days (range: 1-90)."
    )
    additional_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional scenario-specific metadata (e.g. soil moisture start values, reservoir levels)."
    )


class SimulationResponse(BaseModel):
    """
    Standardized payload returned upon initiating a simulation run.
    """
    status: Literal["success"] = Field(
        default="success",
        description="Always 'success' for successful runs."
    )
    message: str = Field(
        ...,
        description="Detailed outcome message of the simulation."
    )
    simulation_id: str = Field(
        ...,
        description="Unique tracking UUID generated for this simulation."
    )
    scenario_type: str = Field(
        ...,
        description="The type of scenario that was simulated."
    )
    metrics: Dict[str, Any] = Field(
        ...,
        description="Key outcome aggregates (e.g. peak heat index, cumulative excess rainfall, drought risk factor)."
    )
    timeline: List[Dict[str, Any]] = Field(
        ...,
        description="Simulated daily time series of climate/environmental parameters for the duration window."
    )
