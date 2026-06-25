"""
Flood Inundation Model.

This module models surface water routing and depth indexes based on digital
elevation models (DEM) and accumulated rainfall.

Classes:
    FloodModel: Evaluates flow direction and water accumulation depths.

TODO:
    * Load and parse local Digital Elevation Models (DEM) from cartographic sources.
    * Implement 2D shallow water equation solver or Manning's routing formula.
"""

from typing import List
from loguru import logger

from app.simulation.climate_state import ClimateState


class FloodModel:
    """
    Simulates overland flow routing and river basin inundation.
    """

    def __init__(self):
        # Default mock elevation values (10x10 grid)
        self.elevation_grid = [
            100.0, 98.0, 95.0, 90.0, 85.0, 80.0, 78.0, 75.0, 72.0, 70.0,
            102.0, 99.0, 96.0, 91.0, 86.0, 81.0, 79.0, 76.0, 73.0, 71.0,
            104.0, 101.0, 98.0, 93.0, 88.0, 83.0, 80.0, 77.0, 74.0, 72.0,
            105.0, 102.0, 99.0, 94.0, 89.0, 84.0, 81.0, 78.0, 75.0, 73.0,
            107.0, 104.0, 101.0, 95.0, 90.0, 85.0, 82.0, 79.0, 76.0, 74.0,
            108.0, 105.0, 102.0, 96.0, 91.0, 86.0, 83.0, 80.0, 77.0, 75.0,
            110.0, 107.0, 104.0, 97.0, 92.0, 87.0, 84.0, 81.0, 78.0, 76.0,
            112.0, 109.0, 106.0, 98.0, 93.0, 88.0, 85.0, 82.0, 79.0, 77.0,
            114.0, 111.0, 108.0, 99.0, 94.0, 89.0, 86.0, 83.0, 80.0, 78.0,
            115.0, 112.0, 109.0, 100.0, 95.0, 90.0, 87.0, 84.0, 81.0, 79.0
        ]

    def run_inundation_routing(self, state: ClimateState, rainfall_mm: float, hours: int) -> List[float]:
        """
        Calculates flood water heights across regional elevation basins.
        
        Mathematical concept:
            1. Derive Slope/Gradient vector field from Digital Elevation Model.
            2. Compute Flow Directions (e.g. D8 routing algorithm).
            3. Run Flow Accumulation weighted by Net Runoff (Rainfall - Infiltration).
            4. Resolve Manning's Equation to determine open channel flow velocities and depths.
            
        Args:
            state: Current climate state representation.
            rainfall_mm: Total precipitation input volume.
            hours: Storm duration index.
            
        Returns:
            List of flood depths in meters per grid cell.
        """
        logger.info(f"Running flood inundation routing for {rainfall_mm}mm over {hours} hours...")
        
        # Grid dimensions match the input state
        cell_count = len(state.precipitation_grid)
        
        # Simple placeholder logic: lower elevation cells accumulate more water.
        # Max elevation is 115.0m, min elevation is 70.0m
        flood_depths = []
        for i in range(cell_count):
            elev = self.elevation_grid[i % len(self.elevation_grid)]
            # Runoff factor increases with rainfall and lower slopes/elevation
            runoff = rainfall_mm * 0.6  # 60% runoff coefficient mock
            
            # Lower elevations accumulate water depth (up to 3.0 meters maximum mock)
            depth = max(0.0, (115.0 - elev) / 45.0) * (runoff / 100.0)
            flood_depths.append(min(5.0, depth))
            
        return flood_depths
