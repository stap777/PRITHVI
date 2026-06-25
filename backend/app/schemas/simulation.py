"""
Digital Twin Simulation Schemas.

This module defines Pydantic validation structures for launching multi-hazard
climate simulation scenarios and retrieving spatial risk analysis indicators.

Classes:
    FloodSimulationParams: Parameters for water inundation maps.
    DroughtSimulationParams: Parameters for soil dryness index calculations.
    CropStressParams: Parameters for agricultural crop yield reduction.
    SimulationRequest: Global request payload parameters for twin runs.
    SimulationMetrics: Yield statistics and hazard indexes response.
    SimulationResponse: Combined outputs returning impact evaluations.

TODO:
    * Support custom elevation model elevation file path overrides in parameters.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FloodSimulationParams(BaseModel):
    """Parameters representing rainfall volume and slope criteria."""
    rainfall_excess_mm: float = Field(default=100.0, ge=0.0, description="Total rainfall runoff volume")
    duration_hours: int = Field(default=24, ge=1, description="Storm duration in hours")
    slope_threshold_pct: float = Field(default=2.5, description="Slope limits below which flooding forms")


class DroughtSimulationParams(BaseModel):
    """Parameters representing dry periods and soil moisture baselines."""
    consecutive_dry_months: int = Field(default=6, ge=1, description="Dry months duration")
    initial_soil_moisture_pct: float = Field(default=45.0, ge=0.0, le=100.0)


class CropStressParams(BaseModel):
    """Parameters defining crop growth stages and targets."""
    crop_type: str = Field(default="rice", description="Target crop (e.g. rice, wheat, maize)")
    growth_stage: str = Field(default="flowering", description="Crop phenology stage")


class SimulationRequest(BaseModel):
    """Input payload to orchestrate digital twin multi-scenario hazard runs."""
    scenario_name: str = Field(
        ...,
        description="IPCC scenario target (e.g. 'SSP2-4.5', 'SSP5-8.5', 'Historical Extreme')"
    )
    region_geojson: Dict[str, Any] = Field(
        ...,
        description="GeoJSON Geometry polygon outlining target Indian state or river basin"
    )
    years_projection: int = Field(default=10, ge=1, le=50, description="Timeline projection span")
    
    # Sub-model parameters (Optional triggers)
    flood_params: Optional[FloodSimulationParams] = None
    drought_params: Optional[DroughtSimulationParams] = None
    crop_params: Optional[CropStressParams] = None


class SimulationMetrics(BaseModel):
    """Output structural calculations for risk evaluation."""
    hazard_index: float = Field(..., ge=0.0, le=1.0, description="Normalized danger value")
    affected_area_sq_km: float = Field(..., description="Clipped land surface area impacted")
    estimated_population_affected: int = Field(..., description="Gridded census population overlay estimate")
    economic_loss_risk: str = Field(..., description="Categorized hazard classification: Low, Medium, High")


class SimulationResponse(BaseModel):
    """Aggregated response containing digital twin simulation results."""
    simulation_id: str
    scenario_name: str
    years_projection: int
    status: str = Field(..., description="Execution status: completed, processing, failed")
    
    # Spatial results summaries
    flood_results: Optional[SimulationMetrics] = None
    drought_results: Optional[SimulationMetrics] = None
    crop_stress_results: Optional[SimulationMetrics] = None
    
    metadata: Dict[str, Any] = Field(
        default={},
        description="Metadata on computational steps, boundary boxes, and execution timings"
    )
