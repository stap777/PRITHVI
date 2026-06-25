"""
Impact Assessment Service.

This service synthesizes raw spatial indices calculated by physics-based simulation
models and overlays them with vulnerability datasets (population maps, economic data)
to calculate human and economic exposure.

Classes:
    ImpactService: Business logic to calculate socio-economic risk parameters.

TODO:
    * Load real population gridded rasters (e.g., GPWv4) to calculate affected counts.
    * Implement spatial intersection logic using geopandas.
"""

from loguru import logger

from app.schemas.simulation import (
    SimulationMetrics, 
    FloodSimulationParams, 
    DroughtSimulationParams, 
    CropStressParams
)
from app.simulation.climate_state import ClimateState
from app.simulation.flood_model import FloodModel
from app.simulation.drought_model import DroughtModel
from app.simulation.agriculture_model import AgricultureModel


class ImpactService:
    """
    Evaluates exposure metrics by combining environmental hazard layers with census overlays.
    """

    def __init__(self):
        # Instantiate physical simulation layers
        self.flood_model = FloodModel()
        self.drought_model = DroughtModel()
        self.agriculture_model = AgricultureModel()

    def assess_flood_impact(self, state: ClimateState, params: FloodSimulationParams) -> SimulationMetrics:
        """
        Runs flood routing and assesses population/infrastructure exposure.
        
        Args:
            state: Active ClimateState representation.
            params: Run configurations for water runoff rates.
            
        Returns:
            SimulationMetrics evaluating flood damages.
        """
        logger.info("Assessing societal impact of flood simulation scenario.")
        
        # Calculate inundation depths
        depth_grid = self.flood_model.run_inundation_routing(
            state=state,
            rainfall_mm=params.rainfall_excess_mm,
            hours=params.duration_hours
        )
        
        # In a real run, we would overlay depth_grid with population raster using rasterio.
        # Placeholder calculation logic:
        affected_area = float(len(depth_grid)) * 1.5 # Mock area conversion
        pop_count = int(affected_area * 150) # Mock density multiplier
        
        hazard_index = min(1.0, (params.rainfall_excess_mm / 300.0))

        return SimulationMetrics(
            hazard_index=hazard_index,
            affected_area_sq_km=affected_area,
            estimated_population_affected=pop_count,
            economic_loss_risk="High" if hazard_index > 0.7 else "Medium"
        )

    def assess_drought_impact(self, state: ClimateState, params: DroughtSimulationParams) -> SimulationMetrics:
        """
        Runs drought indices calculations and assesses agricultural/water supply exposure.
        
        Args:
            state: Active ClimateState representation.
            params: Run configurations for dry periods.
            
        Returns:
            SimulationMetrics evaluating drought index damages.
        """
        logger.info("Assessing regional water scarcity impacts of drought scenario.")
        
        spei_grid = self.drought_model.calculate_spei(
            state=state,
            months_horizon=params.consecutive_dry_months
        )
        
        # Placeholder calculation logic:
        mean_spei = sum(spei_grid) / len(spei_grid) if spei_grid else -1.0
        hazard_index = min(1.0, abs(mean_spei) / 3.0)
        
        affected_area = 15420.5
        pop_count = int(affected_area * 25)

        return SimulationMetrics(
            hazard_index=hazard_index,
            affected_area_sq_km=affected_area,
            estimated_population_affected=pop_count,
            economic_loss_risk="Medium" if hazard_index < 0.6 else "High"
        )

    def assess_crop_impact(self, state: ClimateState, params: CropStressParams) -> SimulationMetrics:
        """
        Calculates crop stress indicators and assesses agricultural yield exposures.
        
        Args:
            state: Active ClimateState representation.
            params: Run configurations targeting crop configurations.
            
        Returns:
            SimulationMetrics evaluating agricultural yield index.
        """
        logger.info(f"Assessing crop yield risks for: {params.crop_type} at stage: {params.growth_stage}.")
        
        stress_grid = self.agriculture_model.calculate_crop_stress(
            state=state,
            crop_type=params.crop_type,
            stage=params.growth_stage
        )
        
        # Placeholder calculation logic:
        mean_stress = sum(stress_grid) / len(stress_grid) if stress_grid else 0.2
        hazard_index = mean_stress
        
        affected_area = 8400.2
        pop_count = int(affected_area * 8) # farm operators

        return SimulationMetrics(
            hazard_index=hazard_index,
            affected_area_sq_km=affected_area,
            estimated_population_affected=pop_count,
            economic_loss_risk="Low" if hazard_index < 0.3 else "Medium"
        )
