"""
Climate Service.

Purpose:
    Contains all business logic and request validations for climate data retrieval.
"""

from datetime import date
from typing import List, Optional
from loguru import logger

from app.repositories.climate_repository import BaseClimateRepository
from app.schemas.enums import ClimateParameter
from app.schemas.common import CommonResponse
from app.schemas.climate import ClimateHistoryResponse, ClimateRecord
from app.exceptions.handlers import DistrictNotFoundError


class ClimateService:
    """
    Coordinates access to climate data repositories and formats results into API contracts.
    """

    def __init__(self, repo: BaseClimateRepository):
        self.repo = repo

    def _validate_location(self, state: str, district: str):
        """
        Validates if the requested district exists. Raises DistrictNotFoundError if not.
        """
        if not self.repo.has_district(state, district):
            logger.warning(f"Validation failed: state={state}, district={district} not found.")
            raise DistrictNotFoundError(
                message=f"District '{district}' in state '{state}' was not found in the supported dataset catalog."
            )

    def get_historical_data(
        self,
        state: str,
        district: str,
        start_date: date,
        end_date: date,
        variables: List[ClimateParameter],
    ) -> ClimateHistoryResponse:
        # Validate location existence
        self._validate_location(state, district)

        # Retrieve records from repository
        records = self.repo.get_history(state, district, start_date, end_date)

        # Mapping enums to model attribute names
        attr_map = {
            ClimateParameter.TEMPERATURE: "temperature",
            ClimateParameter.RAINFALL: "rainfall",
            ClimateParameter.LST: "lst",
            ClimateParameter.SST: "sst",
        }
        param_label_map = {
            ClimateParameter.TEMPERATURE: "Temperature",
            ClimateParameter.RAINFALL: "Rainfall",
            ClimateParameter.LST: "LST",
            ClimateParameter.SST: "SST",
        }

        # Convert records to response format
        formatted_data = []
        for r in records:
            record_dict = {"date": r.date.isoformat()}
            for var in variables:
                attr_name = attr_map[var]
                record_dict[param_label_map[var]] = getattr(r, attr_name)
            formatted_data.append(record_dict)

        # Handle empty result set
        message = (
            "Historical climate data retrieved successfully."
            if formatted_data
            else "No historical records found for the specified parameters and date range."
        )

        return ClimateHistoryResponse(
            status="success",
            message=message,
            state=state,
            district=district,
            start_date=start_date,
            end_date=end_date,
            data=formatted_data,
        )

    def get_current_data(
        self, state: str, district: str, variables: List[ClimateParameter]
    ) -> CommonResponse:
        # Validate location existence
        self._validate_location(state, district)

        # Retrieve current (latest date) record
        record = self.repo.get_current(state, district)

        if not record:
            return CommonResponse(
                status="success",
                message="No current records found for the specified district.",
                data=None,
            )

        # Mapping maps
        attr_map = {
            ClimateParameter.TEMPERATURE: "temperature",
            ClimateParameter.RAINFALL: "rainfall",
            ClimateParameter.LST: "lst",
            ClimateParameter.SST: "sst",
        }
        param_label_map = {
            ClimateParameter.TEMPERATURE: "Temperature",
            ClimateParameter.RAINFALL: "Rainfall",
            ClimateParameter.LST: "LST",
            ClimateParameter.SST: "SST",
        }

        data_payload = {
            "state": record.state,
            "district": record.district,
            "date": record.date.isoformat(),
        }
        for var in variables:
            attr_name = attr_map[var]
            data_payload[param_label_map[var]] = getattr(record, attr_name)

        return CommonResponse(
            status="success",
            message="Current observations retrieved successfully.",
            data=data_payload,
        )
