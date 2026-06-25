"""
Simulation Layer Test Suite.

This module asserts the behavior of physical models (flood, drought, crop stress)
and scenario engine stepping mechanisms.

TODO:
    * Mock vector overlays.
"""

from datetime import datetime
import pytest

from app.simulation.climate_state import ClimateState
from app.simulation.scenario_engine import ScenarioEngine
from app.simulation.flood_model import FloodModel
from app.simulation.drought_model import DroughtModel
from app.simulation.agriculture_model import AgricultureModel


def test_scenario_engine_stepping():
    """Asserts that stepping the scenario engine forward mutates the state variables."""
    engine = ScenarioEngine()
    initial_state = engine.initialize_state("SSP5-8.5", 5)
    
    avg_temp_start = initial_state.average_temperature()
    
    # Step forward by 1 tick (1 year)
    next_state = engine.step_forward(initial_state, "SSP5-8.5")
    
    avg_temp_next = next_state.average_temperature()
    
    # Temperature should have increased under SSP5-8.5 (+0.055C)
    assert avg_temp_next > avg_temp_start
    assert abs(avg_temp_next - avg_temp_start - 0.055) < 1e-4
    assert next_state.timestamp > initial_state.timestamp


def test_flood_inundation_routing():
    """Asserts that lower elevations receive more water in flood models."""
    state = ClimateState(
        timestamp=datetime.now(),
        temperature_grid=[25.0] * 100,
        precipitation_grid=[10.0] * 100,
        soil_moisture_grid=[50.0] * 100,
        evapotranspiration_grid=[3.5] * 100
    )
    
    flood_model = FloodModel()
    # Run heavy storm simulation: 150mm over 6 hours
    flood_depths = flood_model.run_inundation_routing(state, rainfall_mm=150.0, hours=6)
    
    assert len(flood_depths) == 100
    # Lower elevation grid cell (index 9, elev=70m) should have deeper flooding
    # than higher elevation cell (index 0, elev=100m)
    assert flood_depths[9] > flood_depths[0]


def test_drought_spei_indices():
    """Asserts SPEI calculations scale with water balance values."""
    state = ClimateState(
        timestamp=datetime.now(),
        temperature_grid=[25.0] * 100,
        # High evaporation relative to rain (dry conditions)
        precipitation_grid=[1.0] * 100,
        evapotranspiration_grid=[8.0] * 100,
        soil_moisture_grid=[20.0] * 100
    )
    
    drought_model = DroughtModel()
    spei_indices = drought_model.calculate_spei(state, months_horizon=6)
    
    assert len(spei_indices) == 100
    # Negative SPEI value indicates drought conditions
    assert all(idx < 0 for idx in spei_indices)


def test_crop_stress_factors():
    """Asserts crop stress increases when temperatures exceed optimal bounds."""
    # Optimal rice temperature is 20-35C
    good_state = ClimateState(
        timestamp=datetime.now(),
        temperature_grid=[28.0] * 100,
        precipitation_grid=[10.0] * 100,
        evapotranspiration_grid=[3.5] * 100,
        soil_moisture_grid=[60.0] * 100
    )
    
    # Extreme heat state (42C)
    extreme_state = ClimateState(
        timestamp=datetime.now(),
        temperature_grid=[42.0] * 100,
        precipitation_grid=[0.0] * 100,
        evapotranspiration_grid=[9.0] * 100,
        soil_moisture_grid=[15.0] * 100
    )
    
    agri_model = AgricultureModel()
    
    good_stress = agri_model.calculate_crop_stress(good_state, "rice", "flowering")
    bad_stress = agri_model.calculate_crop_stress(extreme_state, "rice", "flowering")
    
    # Extreme heat stress should be significantly higher than optimal temperature stress
    assert good_stress[0] < bad_stress[0]
