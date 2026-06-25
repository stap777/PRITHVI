"""
Climate State Model.

This module defines the ClimateState class, representing a temporal snapshot of the 
geospatial environment (atmospheric, hydrological, and agricultural variables)
at a specific tick of the simulation.

Classes:
    ClimateState: Structure containing spatial grids and time indicators.

TODO:
    * Shift grid storage from list of floats to numpy.ndarray for speed.
    * Add serialization checks for netCDF exporting.
"""

from typing import List, Dict, Any
from datetime import datetime


class ClimateState:
    """
    Encapsulates the state of the microclimate grid during a digital twin run.
    
    Attributes:
        timestamp: Simulation time coordinate.
        temperature_grid: Gridded temperature values (Celsius) across region.
        precipitation_grid: Gridded precipitation values (mm/day).
        soil_moisture_grid: Relative water content percentiles of topsoil layer.
        evapotranspiration_grid: Water evaporation values (mm/day).
    """

    def __init__(
        self,
        timestamp: datetime,
        temperature_grid: List[float],
        precipitation_grid: List[float],
        soil_moisture_grid: List[float],
        evapotranspiration_grid: List[float],
        metadata: Dict[str, Any] = None
    ):
        self.timestamp: datetime = timestamp
        self.temperature_grid: List[float] = temperature_grid
        self.precipitation_grid: List[float] = precipitation_grid
        self.soil_moisture_grid: List[float] = soil_moisture_grid
        self.evapotranspiration_grid: List[float] = evapotranspiration_grid
        self.metadata: Dict[str, Any] = metadata or {}

    def get_grid_dimensions(self) -> Dict[str, int]:
        """
        Returns grid structure metadata.
        """
        return {
            "length": len(self.temperature_grid),
            "columns": self.metadata.get("cols", 100),
            "rows": self.metadata.get("rows", 100)
        }

    def average_temperature(self) -> float:
        """
        Calculates region-wide average temperature.
        """
        if not self.temperature_grid:
            return 0.0
        return sum(self.temperature_grid) / len(self.temperature_grid)

    def total_precipitation(self) -> float:
        """
        Calculates total regional precipitation sum.
        """
        return sum(self.precipitation_grid)
