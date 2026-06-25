"""
Digital Twin Scenario Engine.

This module initializes base climate states and applies transition pathways
(e.g., SSP2-4.5, SSP5-8.5) to simulate future climate states over decadal projections.

Classes:
    ScenarioEngine: Main engine to mutate ClimateState records over projection periods.

TODO:
    * Load actual CMIP6 ensemble models for India's regional downscaling.
    * Incorporate spatial elevation multipliers into temperature regressions.
    """

from datetime import datetime, timedelta
from loguru import logger

from app.simulation.climate_state import ClimateState


class ScenarioEngine:
    """
    Main driver of climate mutations based on target greenhouse gas emission curves.
    """

    def __init__(self):
        # Default scaling coefficients for temperature/rainfall increases per year
        self.scenario_delta_factors = {
            "SSP1-2.6": {"temp_inc": 0.015, "precip_mult": 1.001},
            "SSP2-4.5": {"temp_inc": 0.025, "precip_mult": 1.003},
            "SSP5-8.5": {"temp_inc": 0.055, "precip_mult": 1.008},
            "Historical Extreme": {"temp_inc": 0.005, "precip_mult": 1.000}
        }

    def initialize_state(self, scenario: str, years: int) -> ClimateState:
        """
        Creates starting baseline state of India's grid.
        
        Args:
            scenario: Target pathway.
            years: Total simulation years.
            
        Returns:
            ClimateState representing the initial state.
        """
        logger.info(f"Initializing baseline ClimateState for {scenario} over {years} years.")
        
        # Populate dummy grids (10x10 cell mock area for speed)
        cell_count = 100
        temp_grid = [27.5] * cell_count # average India temperature
        precip_grid = [5.0] * cell_count
        moisture_grid = [50.0] * cell_count
        evap_grid = [3.5] * cell_count

        return ClimateState(
            timestamp=datetime.now(),
            temperature_grid=temp_grid,
            precipitation_grid=precip_grid,
            soil_moisture_grid=moisture_grid,
            evapotranspiration_grid=evap_grid,
            metadata={"cols": 10, "rows": 10, "scenario": scenario}
        )

    def step_forward(self, state: ClimateState, scenario_name: str) -> ClimateState:
        """
        Mutates the ClimateState variables by one year under scenario constraints.
        
        Args:
            state: Current simulation climate state.
            scenario_name: Target path (SSP5-8.5 etc.).
            
        Returns:
            Mutated ClimateState representation.
        """
        factors = self.scenario_delta_factors.get(scenario_name, {"temp_inc": 0.01, "precip_mult": 1.0})
        logger.debug(f"Applying step mutators: Temp +{factors['temp_inc']}C, Rain x{factors['precip_mult']}")

        # Apply climate drift parameters
        new_temp = [t + factors["temp_inc"] for t in state.temperature_grid]
        new_precip = [p * factors["precip_mult"] for p in state.precipitation_grid]
        
        # Simple feedback mechanism: warmer temperature decreases soil moisture
        new_moisture = [max(0.0, m - (factors["temp_inc"] * 10)) for m in state.soil_moisture_grid]
        new_evap = [e + (factors["temp_inc"] * 0.1) for e in state.evapotranspiration_grid]

        return ClimateState(
            timestamp=state.timestamp + timedelta(days=365),
            temperature_grid=new_temp,
            precipitation_grid=new_precip,
            soil_moisture_grid=new_moisture,
            evapotranspiration_grid=new_evap,
            metadata=state.metadata
        )
