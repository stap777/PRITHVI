"""
Unit tests for the IMD NetCDF loader and ClimateRepository integration.
"""

from datetime import date
from pathlib import Path
import pytest
import numpy as np

from app.config.settings import settings
from app.pipeline.imd_loader import IMDNetCDFLoader
from app.repositories.climate_repository import ClimateRepository
from app.schemas.climate import RainfallObservation, ClimateRecord


@pytest.fixture
def dataset_path() -> Path:
    possible_paths = [
        settings.DATA_DIR.resolve().parent.parent / "dataset" / "RF25_ind2025_rfp25.nc",
        settings.DATA_DIR.resolve().parent / "dataset" / "RF25_ind2025_rfp25.nc",
        Path("../dataset/RF25_ind2025_rfp25.nc"),
        Path("dataset/RF25_ind2025_rfp25.nc")
    ]
    for p in possible_paths:
        if p.exists():
            return p
    raise FileNotFoundError("RF25_ind2025_rfp25.nc not found in expected locations.")


@pytest.fixture
def loader(dataset_path) -> IMDNetCDFLoader:
    loader_instance = IMDNetCDFLoader(dataset_path)
    yield loader_instance
    loader_instance.close()


def test_loader_initialization(loader):
    """Verifies that the dataset is loaded and coordinate grids are parsed."""
    lats, lons = loader.get_coordinates()
    assert len(lats) > 0
    assert len(lons) > 0
    
    times = loader.get_time_dimension()
    assert len(times) == 365
    assert all(isinstance(t, date) for t in times)
    assert times[0] == date(2025, 1, 1)
    assert times[-1] == date(2025, 12, 31)


def test_loader_get_rainfall_success(loader):
    """Verifies retrieval of a valid daily rainfall observation."""
    # Query a point in Ratnagiri region (Lat 17.0, Lon 73.25)
    query_date = date(2025, 6, 15)
    val = loader.get_rainfall(17.0, 73.25, query_date)
    assert val is not None
    assert isinstance(val, float)
    assert val >= 0.0


def test_loader_get_rainfall_missing_value(loader):
    """Verifies that missing values (e.g. ocean coordinate) return None."""
    # Lat 6.5, Lon 66.5 is in the ocean and masked in the dataset
    query_date = date(2025, 6, 15)
    val = loader.get_rainfall(6.5, 66.5, query_date)
    assert val is None


def test_loader_get_rainfall_out_of_bounds(loader):
    """Verifies that coordinates far out of the grid bounds return None."""
    query_date = date(2025, 6, 15)
    # Latitude outside India (e.g., 50.0 N)
    val = loader.get_rainfall(50.0, 73.25, query_date)
    assert val is None


def test_loader_get_rainfall_invalid_date(loader):
    """Verifies that dates outside the dataset range (2025) return None."""
    val = loader.get_rainfall(17.0, 73.25, date(2026, 6, 15))
    assert val is None


def test_loader_get_rainfall_observation(loader):
    """Verifies retrieval of the strongly-typed RainfallObservation domain model."""
    query_date = date(2025, 6, 15)
    obs = loader.get_rainfall_observation(17.0, 73.25, query_date)
    assert obs is not None
    assert isinstance(obs, RainfallObservation)
    assert obs.date == query_date
    assert obs.latitude == 17.0
    assert obs.longitude == 73.25
    assert obs.rainfall_mm >= 0.0


def test_repository_netcdf_fallback_flow():
    """Verifies that the ClimateRepository retrieves real rainfall for 2025 and mock for 2026."""
    repo = ClimateRepository()
    
    # 1. Query for 2025 (should fetch from NetCDF loader)
    history_2025 = repo.get_history(
        state="Maharashtra",
        district="Ratnagiri",
        start_date=date(2025, 6, 1),
        end_date=date(2025, 6, 5)
    )
    assert len(history_2025) == 5
    for record in history_2025:
        assert isinstance(record, ClimateRecord)
        assert record.state == "Maharashtra"
        assert record.district == "Ratnagiri"
        assert record.rainfall is not None
        # Temperature/LST/SST are not in NetCDF so they should be None
        assert record.temperature is None
        assert record.lst is None
        assert record.sst is None
        
    # 2. Query for 2026 (should fetch from mock JSON fallback)
    history_2026 = repo.get_history(
        state="Maharashtra",
        district="Ratnagiri",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 5)
    )
    assert len(history_2026) == 5
    for record in history_2026:
        assert isinstance(record, ClimateRecord)
        assert record.state == "Maharashtra"
        assert record.district == "Ratnagiri"
        assert record.rainfall is not None
        assert record.temperature is not None  # Mock data contains temperature
