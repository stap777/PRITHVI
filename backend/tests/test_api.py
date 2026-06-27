"""
API Controller Test Suite.

Purpose:
    This module asserts the responses of REST controllers (health check and root index)
    using FastAPI's TestClient.

Future Responsibilities:
    * Expand test assertions to cover database connection drop behaviors.
    * Add automated benchmark checks for API response times.

TODO:
    * Mock external service connectivity states to verify degraded health status responses.
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


def test_direct_health_endpoint():
    """Asserts direct /health endpoint reports back status, service name, and version."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["service"] == "PRITHVI Backend"
    assert json_data["version"] == "0.1.0"


def test_prefixed_health_endpoint():
    """Asserts api/v1 prefixed health endpoint reports back status, service name, and version."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["service"] == "PRITHVI Backend"
    assert json_data["version"] == "0.1.0"
