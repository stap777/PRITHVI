"""
Climate Repository.

Purpose:
    Defines the contract and implementation for accessing climate dataset records.
    Currently backed by a mock JSON file, but prepared to be swapped for real NetCDF/IMD datasets.
"""

import json
from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import List, Optional
from loguru import logger

from app.config.settings import settings
from app.schemas.climate import ClimateRecord


class BaseClimateRepository(ABC):
    """
    Abstract Base Class outlining the Climate Repository contract.
    """

    @abstractmethod
    def get_history(
        self, state: str, district: str, start_date: date, end_date: date
    ) -> List[ClimateRecord]:
        """
        Retrieves a list of historical climate records matching the criteria.
        """
        pass

    @abstractmethod
    def get_current(self, state: str, district: str) -> Optional[ClimateRecord]:
        """
        Retrieves the latest single climate record by date for the location.
        """
        pass

    @abstractmethod
    def has_district(self, state: str, district: str) -> bool:
        """
        Checks if the state/district combination exists in the dataset.
        """
        pass


class ClimateRepository(BaseClimateRepository):
    """
    JSON and NetCDF backed repository loading mock records and real IMD NetCDF observations.
    """

    def __init__(self):
        self._records: List[ClimateRecord] = []
        self._load_mock_data()
        
        # Initialize IMD NetCDF Loader
        # Robustly resolve the NetCDF dataset path across different running directories
        possible_paths = [
            settings.DATA_DIR.resolve().parent.parent / "dataset" / "RF25_ind2025_rfp25.nc",
            settings.DATA_DIR.resolve().parent / "dataset" / "RF25_ind2025_rfp25.nc",
            Path("../dataset/RF25_ind2025_rfp25.nc"),
            Path("dataset/RF25_ind2025_rfp25.nc")
        ]
        netcdf_path = None
        for p in possible_paths:
            if p.exists():
                netcdf_path = p
                break
        if not netcdf_path:
            netcdf_path = possible_paths[0]
            
        from app.pipeline.imd_loader import IMDNetCDFLoader
        self.loader = IMDNetCDFLoader(netcdf_path)
        
        # Hardcoded district coordinate mapping (avoids dynamic GIS polygon lookups in this sprint)
        self._district_coords = {
            ("maharashtra", "ratnagiri"): (17.0, 73.25)
        }

    def _load_mock_data(self):
        file_path = settings.DATA_DIR / "mock" / "climate_data.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self._records = [
                    ClimateRecord.model_validate(item) for item in raw_data
                ]
            logger.info(
                f"Successfully loaded {len(self._records)} mock climate records from {file_path}"
            )
        except Exception as e:
            logger.error(f"Failed to load mock climate data from {file_path}: {e}")
            self._records = []

    def _is_in_loader_range(self, start_date: date, end_date: date) -> bool:
        try:
            times = self.loader.get_time_dimension()
            if not times:
                return False
            # Check overlap between query range and NetCDF time dimension
            return start_date <= times[-1] and end_date >= times[0]
        except Exception:
            return False

    def get_history(
        self, state: str, district: str, start_date: date, end_date: date
    ) -> List[ClimateRecord]:
        state_norm = state.strip().lower()
        dist_norm = district.strip().lower()
        
        # Check if coordinates map contains the district
        coords = self._district_coords.get((state_norm, dist_norm))
        
        # If coordinates exist and date range overlaps with the NetCDF dataset (2025)
        if coords and self._is_in_loader_range(start_date, end_date):
            lat, lon = coords
            records = []
            try:
                times = self.loader.get_time_dimension()
                loader_start = max(start_date, times[0])
                loader_end = min(end_date, times[-1])
                
                from datetime import timedelta
                current = loader_start
                while current <= loader_end:
                    val = self.loader.get_rainfall(lat, lon, current)
                    records.append(
                        ClimateRecord(
                            date=current,
                            state=state,
                            district=district,
                            rainfall=val
                        )
                    )
                    current += timedelta(days=1)
                return records
            except Exception as e:
                logger.error(f"Error reading historical rainfall from NetCDF: {e}")

        # Fallback to mock JSON data
        matching = []
        for r in self._records:
            if (
                r.state.strip().lower() == state_norm
                and r.district.strip().lower() == dist_norm
                and start_date <= r.date <= end_date
            ):
                matching.append(r)
        return matching

    def get_current(self, state: str, district: str) -> Optional[ClimateRecord]:
        state_norm = state.strip().lower()
        dist_norm = district.strip().lower()
        
        records = []
        # Query mock database
        for r in self._records:
            if (
                r.state.strip().lower() == state_norm
                and r.district.strip().lower() == dist_norm
            ):
                records.append(r)
                
        # Query NetCDF loader if coordinates exist
        coords = self._district_coords.get((state_norm, dist_norm))
        if coords:
            lat, lon = coords
            try:
                times = self.loader.get_time_dimension()
                if times:
                    latest_date = times[-1]
                    val = self.loader.get_rainfall(lat, lon, latest_date)
                    if val is not None:
                        records.append(
                            ClimateRecord(
                                date=latest_date,
                                state=state,
                                district=district,
                                rainfall=val
                            )
                        )
            except Exception as e:
                logger.error(f"Error fetching current observation from NetCDF: {e}")
                
        if not records:
            return None
            
        # Return record with the maximum date value (e.g. 2026 mock data over 2025 NetCDF data)
        return max(records, key=lambda r: r.date)

    def has_district(self, state: str, district: str) -> bool:
        state_norm = state.strip().lower()
        dist_norm = district.strip().lower()
        if (state_norm, dist_norm) in self._district_coords:
            return True
        for r in self._records:
            if (
                r.state.strip().lower() == state_norm
                and r.district.strip().lower() == dist_norm
            ):
                return True
        return False

