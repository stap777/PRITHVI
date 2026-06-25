"""
Drought Analysis Model.

This module calculates Standardized Precipitation Index (SPI) and 
Standardized Precipitation Evapotranspiration Index (SPEI) to classify 
drought severity stages across region grids.

Classes:
    DroughtModel: Performs spatial drought index estimations.

TODO:
    * Implement log-logistic probability distribution fitting for water balances.
    * Incorporate historical precipitation lookup arrays for standardization.
"""

from typing import List
from loguru import logger

from app.simulation.climate_state import ClimateState


class DroughtModel:
    """
    Calculates statistical climatological dry indices (SPI, SPEI).
    """

    def __init__(self):
        pass

    def calculate_spei(self, state: ClimateState, months_horizon: int) -> List[float]:
        """
        Calculates Standardized Precipitation Evapotranspiration Index (SPEI).
        
        Mathematical concept:
            1. Calculate daily Water Balance (D = Precipitation - Potential Evapotranspiration).
            2. Accumulate D over target month window (e.g. 3, 6, or 12 months).
            3. Fit D values to a probability distribution (usually Log-Logistic).
            4. Transform cumulative probabilities to standard normal distributions (mean=0, std=1).
            
        Args:
            state: Current simulation climate state representation.
            months_horizon: Aggregation timespan (e.g. SPEI-3, SPEI-6).
            
        Returns:
            List of SPEI index values per grid cell (-3.0 to +3.0 scale).
        """
        logger.info(f"Calculating SPEI-{months_horizon} index across active grid points.")
        
        spei_grid = []
        for precip, evap in zip(state.precipitation_grid, state.evapotranspiration_grid):
            # Water balance index
            water_balance = precip - evap
            
            # Placeholder mock mapping:
            # map water balance to typical SPEI values (-3.0 = extreme drought, 3.0 = extremely wet)
            mock_spei = (water_balance - 1.5) / 2.0
            # Clamp between limits
            mock_spei = max(-3.0, min(3.0, mock_spei))
            spei_grid.append(mock_spei)
            
        return spei_grid

    def calculate_spi(self, state: ClimateState, months_horizon: int) -> List[float]:
        """
        Calculates Standardized Precipitation Index (SPI) using only rainfall datasets.
        
        Args:
            state: Current climate state representation.
            months_horizon: Aggregation timespan.
        """
        logger.info(f"Calculating SPI-{months_horizon} index...")
        
        # Mock calculation:
        spi_grid = [(p - 5.0) / 3.0 for p in state.precipitation_grid]
        return [max(-3.0, min(3.0, s)) for s in spi_grid]
