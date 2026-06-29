"""
Climate Flow Integration and Unit Tests.

Purpose:
    Asserts the correct behavior of the Climate module components (API, Service, Repository)
    working end-to-end with mock datasets.
"""

from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


def test_history_retrieval_success():
    """Verifies that a valid query returns 200 OK and correct records for Ratnagiri."""
    response = client.get(
        "/api/v1/climate/history",
        params={
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "start_date": "2026-06-01",
            "end_date": "2026-06-05",
            "variables": ["Temperature", "Rainfall"]
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["state"] == "Maharashtra"
    assert json_data["district"] == "Ratnagiri"
    assert len(json_data["data"]) == 5
    # Check first record structure
    first_record = json_data["data"][0]
    assert first_record["date"] == "2026-06-01"
    assert "Temperature" in first_record
    assert "Rainfall" in first_record
    # LST and SST should be excluded since they weren't requested
    assert "LST" not in first_record
    assert "SST" not in first_record


def test_current_retrieval_success():
    """Verifies that current query returns the most recent record by date (2026-06-15)."""
    response = client.get(
        "/api/v1/climate/current",
        params={
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "variables": ["Temperature", "Rainfall", "LST", "SST"]
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["state"] == "Maharashtra"
    assert json_data["data"]["district"] == "Ratnagiri"
    # Expect the latest date (2026-06-15)
    assert json_data["data"]["date"] == "2026-06-15"
    assert json_data["data"]["Temperature"] == 29.5
    assert json_data["data"]["Rainfall"] == 3.0


def test_district_not_found():
    """Verifies that querying a non-existent state/district combo returns 404."""
    response = client.get(
        "/api/v1/climate/current",
        params={
            "state": "Maharashtra",
            "district": "Mumbai",
            "variables": ["Temperature"]
        }
    )
    assert response.status_code == 404
    json_data = response.json()
    assert json_data["status"] == "error"
    assert "not found" in json_data["message"]
    assert "timestamp" in json_data


def test_empty_result_set():
    """Verifies that querying dates out-of-bounds returns 200 OK with empty data list."""
    response = client.get(
        "/api/v1/climate/history",
        params={
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "start_date": "2026-05-01",
            "end_date": "2026-05-15",
            "variables": ["Temperature"]
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert len(json_data["data"]) == 0
    assert "No historical records found" in json_data["message"]


def test_invalid_dates_validation():
    """Verifies that start_date > end_date returns 422 Unprocessable Content/Entity."""
    response = client.get(
        "/api/v1/climate/history",
        params={
            "state": "Maharashtra",
            "district": "Ratnagiri",
            "start_date": "2026-06-15",
            "end_date": "2026-06-01",
            "variables": ["Temperature"]
        }
    )
    assert response.status_code == 422
    json_data = response.json()
    assert json_data["status"] == "error"
    assert "Validation failed" in json_data["message"] or "validation" in json_data["message"].lower()
