"""
Agriculture Impact Model.

This module models crop stress and yield impacts using climate inputs
(temperature, precipitation, soil moisture) and agricultural parameters.

Classes:
    AgricultureModel: Models agricultural health based on climate grids.

TODO:
    * Implement Crop Water Requirement (CWR) FAO-56 Penman-Monteith equation.
    * Load GIS crop cover masks (ISRO/Bhuvan datasets) to filter arable grids.
"""

from typing import List
from loguru import logger

from app.simulation.climate_state import ClimateState
from app.config.constants import CROP_TEMPERATURE_THRESHOLDS


class AgricultureModel:
    """
    Simulates agricultural yield stress and soil moisture deficits.
    """

    def __init__(self):
        # Default Crop vulnerability coefficients
        self.water_sensitivity_index = {
            "rice": 1.1,
            "wheat": 1.0,
            "maize": 1.25
        }

    def calculate_crop_stress(self, state: ClimateState, crop_type: str, stage: str) -> List[float]:
        """
        Calculates crop stress levels (0.0 = no stress, 1.0 = maximum stress).
        
        Args:
            state: Current digital twin climate state grid.
            crop_type: Target crop (rice, wheat, etc.).
            stage: Crop phenological development stage (e.g. seedling, flowering, maturity).
            
        Returns:
            List of stress coefficients per grid cell.
        """
        logger.info(f"Running AgricultureModel stress calculations for '{crop_type}'...")
        
        crop_limits = CROP_TEMPERATURE_THRESHOLDS.get(
            crop_type, 
            {"min_optimal": 15.0, "max_optimal": 30.0, "critical_maximum": 38.0}
        )
        sensitivity = self.water_sensitivity_index.get(crop_type, 1.0)
        
        stress_grid = []
        for temp, moisture in zip(state.temperature_grid, state.soil_moisture_grid):
            # 1. Temperature Stress: Increases as temperature goes beyond optimal threshold
            temp_stress = 0.0
            if temp > crop_limits["max_optimal"]:
                diff = temp - crop_limits["max_optimal"]
                range_limit = crop_limits["critical_maximum"] - crop_limits["max_optimal"]
                temp_stress = min(1.0, diff / range_limit)
            elif temp < crop_limits["min_optimal"]:
                temp_stress = 0.2 # Cold stress mockup
                
            # 2. Moisture Stress: Increases as soil moisture goes below 40%
            moisture_stress = 0.0
            if moisture < 40.0:
                moisture_stress = (40.0 - moisture) / 40.0
                
            # Combine indices with sensitivity scaling
            total_stress = min(1.0, (temp_stress * 0.4 + moisture_stress * 0.6) * sensitivity)
            stress_grid.append(total_stress)
            
        return stress_grid
