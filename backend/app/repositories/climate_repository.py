"""
Climate Repository.

Purpose:
    Defines the contract and implementation for accessing climate dataset records.
    Currently backed by a mock JSON file, but prepared to be swapped for real NetCDF/IMD datasets.
"""

import json
from abc import ABC, abstractmethod
from datetime import date
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
    JSON-backed repository loading mock climate records into memory at startup.
    """

    def __init__(self):
        self._records: List[ClimateRecord] = []
        self._load_mock_data()

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

    def get_history(
        self, state: str, district: str, start_date: date, end_date: date
    ) -> List[ClimateRecord]:
        state_norm = state.strip().lower()
        dist_norm = district.strip().lower()
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
        matching = []
        for r in self._records:
            if (
                r.state.strip().lower() == state_norm
                and r.district.strip().lower() == dist_norm
            ):
                matching.append(r)
        if not matching:
            return None
        # Retrieve the record with the maximum date value
        return max(matching, key=lambda r: r.date)

    def has_district(self, state: str, district: str) -> bool:
        state_norm = state.strip().lower()
        dist_norm = district.strip().lower()
        for r in self._records:
            if (
                r.state.strip().lower() == state_norm
                and r.district.strip().lower() == dist_norm
            ):
                return True
        return False
