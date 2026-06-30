"""
API Contract Verification Test Suite.

Purpose:
    Validates that request parameters and request bodies are correctly validated
    by FastAPI / Pydantic, and checks that stub endpoints return HTTP 501.
"""

from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


# ----------------------------------------------------
# Climate History Endpoint (/api/v1/climate/history)
# ----------------------------------------------------

def test_climate_history_success_implemented():
    """Asserts that a valid historical request returns 200 OK."""
    response = client.get(
        "/api/v1/climate/history",
        params={
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "start_date": "2026-06-01",
            "end_date": "2026-06-10",
            "variables": ["Temperature", "Rainfall"]
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_climate_history_missing_params():
    """Asserts that missing required parameters returns 422 Unprocessable Entity."""
    response = client.get("/api/v1/climate/history")
    assert response.status_code == 422


def test_climate_history_invalid_date_range():
    """Asserts that start_date > end_date returns 422 Unprocessable Entity."""
    response = client.get(
        "/api/v1/climate/history",
        params={
            "state": "Maharashtra",
            "district": "Pune",
            "start_date": "2023-01-10",
            "end_date": "2023-01-01",
            "variables": ["Temperature"]
        }
    )
    assert response.status_code == 422
    assert "start_date must be before or equal to end_date" in str(response.json())


def test_climate_history_invalid_parameter():
    """Asserts that unsupported variables trigger 422 validation failure."""
    response = client.get(
        "/api/v1/climate/history",
        params={
            "state": "Maharashtra",
            "district": "Pune",
            "start_date": "2023-01-01",
            "end_date": "2023-01-10",
            "variables": ["InvalidParameter"]
        }
    )
    assert response.status_code == 422


# ----------------------------------------------------
# Climate Current Endpoint (/api/v1/climate/current)
# ----------------------------------------------------

def test_climate_current_success_implemented():
    """Asserts that a valid current request returns 200 OK."""
    response = client.get(
        "/api/v1/climate/current",
        params={
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "variables": ["LST", "SST"]
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_climate_current_validation_failure():
    """Asserts validation failure if state/district/variables are missing or invalid."""
    response = client.get(
        "/api/v1/climate/current",
        params={
            "state": "",
            "district": "Pune",
            "variables": ["InvalidParameter"]
        }
    )
    assert response.status_code == 422


# ----------------------------------------------------
# Climate Overview Endpoint (/api/v1/climate/overview)
# ----------------------------------------------------

def test_climate_overview_success_stub():
    """Asserts that a valid overview dashboard request returns 501 Not Implemented."""
    response = client.get(
        "/api/v1/climate/overview",
        params={
            "state": "Maharashtra",
            "district": "Pune"
        }
    )
    assert response.status_code == 501
    assert "Dashboard overview aggregation service is not implemented." in response.json()["detail"]


def test_climate_overview_validation_failure():
    """Asserts validation fails for short State name."""
    response = client.get(
        "/api/v1/climate/overview",
        params={
            "state": "M",
            "district": "Pune"
        }
    )
    assert response.status_code == 422


# ----------------------------------------------------
# Climate Predictions Endpoint (/api/v1/climate/predictions)
# ----------------------------------------------------

def test_climate_predictions_success_stub():
    """Asserts that a valid forecast request returns 501 Not Implemented."""
    response = client.get(
        "/api/v1/climate/predictions",
        params={
            "state": "Maharashtra",
            "district": "Pune",
            "horizon_days": 30,
            "variables": ["Temperature", "Rainfall"]
        }
    )
    assert response.status_code == 501
    assert "ML Prediction service integration is not implemented." in response.json()["detail"]


def test_climate_predictions_invalid_horizon():
    """Asserts that an out-of-range forecast horizon (e.g. 400 days) returns 422."""
    response = client.get(
        "/api/v1/climate/predictions",
        params={
            "state": "Maharashtra",
            "district": "Pune",
            "horizon_days": 400,
            "variables": ["Temperature"]
        }
    )
    assert response.status_code == 422


# ----------------------------------------------------
# Climate Simulate Endpoint (/api/v1/climate/simulate)
# ----------------------------------------------------

def test_climate_simulate_success_stub():
    """Asserts that a valid simulation trigger request returns 501 Not Implemented."""
    response = client.post(
        "/api/v1/climate/simulate",
        json={
            "scenario_type": "extreme_rainfall",
            "state": "Maharashtra",
            "district": "Pune",
            "intensity_multiplier": 1.8,
            "duration_days": 10
        }
    )
    assert response.status_code == 501
    assert "Digital twin simulation engine is not implemented." in response.json()["detail"]


def test_climate_simulate_invalid_intensity():
    """Asserts that invalid intensity multiplier (e.g. negative or too high) fails validation."""
    response = client.post(
        "/api/v1/climate/simulate",
        json={
            "scenario_type": "extreme_rainfall",
            "state": "Maharashtra",
            "district": "Pune",
            "intensity_multiplier": 10.0,  # Max is 5.0
            "duration_days": 10
        }
    )
    assert response.status_code == 422


def test_climate_simulate_invalid_scenario():
    """Asserts that invalid scenario type triggers 422."""
    response = client.post(
        "/api/v1/climate/simulate",
        json={
            "scenario_type": "super_typhoon",  # Not in allowed literals
            "state": "Maharashtra",
            "district": "Pune",
            "intensity_multiplier": 1.0,
            "duration_days": 5
        }
    )
    assert response.status_code == 422


# ----------------------------------------------------
# Metadata Endpoints (/api/v1/metadata/...)
# ----------------------------------------------------

def test_metadata_states_success_stub():
    """Asserts that listing states returns 501 Not Implemented."""
    response = client.get("/api/v1/metadata/states")
    assert response.status_code == 501
    assert "Metadata repository service is not implemented." in response.json()["detail"]


def test_metadata_districts_success_stub():
    """Asserts that listing districts (with optional filter) returns 501 Not Implemented."""
    response = client.get("/api/v1/metadata/districts", params={"state": "Karnataka"})
    assert response.status_code == 501
    assert "Metadata repository service is not implemented." in response.json()["detail"]


def test_metadata_parameters_success_stub():
    """Asserts that listing parameters returns 501 Not Implemented."""
    response = client.get("/api/v1/metadata/parameters")
    assert response.status_code == 501
    assert "Metadata repository service is not implemented." in response.json()["detail"]
