"""
API Controller Test Suite.

This module asserts the responses of REST controllers (health, climate, prediction,
simulation) using FastAPI's TestClient.

TODO:
    * Mock external database dependencies during testing.
"""

from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Asserts root details page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert "environment" in json_data


def test_health_endpoint():
    """Asserts system dependencies check reports back properly."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert "services" in json_data
    assert json_data["services"]["api_server"] == "online"


def test_climate_history_endpoint():
    """Asserts historical data is returned with structured attributes."""
    response = client.get("/api/v1/climate/history?lat=20.0&lon=75.0&start_year=2000&end_year=2002")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["latitude"] == 20.0
    assert json_data["longitude"] == 75.0
    assert len(json_data["data"]) > 0
    assert "temperature" in json_data["data"][0]


def test_prediction_forecast_endpoint():
    """Asserts triggering forecasting models returns predictions list."""
    payload = {
        "latitude": 20.0,
        "longitude": 75.0,
        "target_metric": "surface_temperature",
        "horizon_months": 6
    }
    response = client.post("/api/v1/prediction/forecast", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["target_metric"] == "surface_temperature"
    assert len(json_data["predictions"]) == 6
    assert "predicted_value" in json_data["predictions"][0]


def test_simulation_run_endpoint():
    """Asserts triggering digital twin scenario simulation runs is accepted."""
    payload = {
        "scenario_name": "SSP5-8.5",
        "region_geojson": {
            "type": "Polygon",
            "coordinates": [[[70.0, 15.0], [72.0, 15.0], [72.0, 17.0], [70.0, 17.0], [70.0, 15.0]]]
        },
        "years_projection": 5,
        "flood_params": {
            "rainfall_excess_mm": 120.0,
            "duration_hours": 12
        }
    }
    response = client.post("/api/v1/simulation/run", json=payload)
    assert response.status_code == 202
    json_data = response.json()
    assert json_data["simulation_id"] is not None
    assert json_data["status"] == "completed"
    assert json_data["flood_results"] is not None
