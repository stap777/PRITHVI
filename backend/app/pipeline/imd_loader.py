"""
IMD NetCDF Data Loader.

Purpose:
    Handles reading gridded climate observations from IMD NetCDF files.
"""

from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple
import numpy as np
import pandas as pd
import xarray as xr
from loguru import logger

from app.schemas.climate import RainfallObservation


class IMDNetCDFLoader:
    """
    Loader responsible for opening and extracting rainfall data from IMD NetCDF datasets.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._dataset: Optional[xr.Dataset] = None
        self._lats: Optional[np.ndarray] = None
        self._lons: Optional[np.ndarray] = None
        self._times: Optional[List[date]] = None
        self._load_dataset()

    def _load_dataset(self):
        """
        Opens the NetCDF file and pre-loads the coordinate dimensions into memory.
        """
        if not self.file_path.exists():
            logger.error(f"IMD NetCDF file not found at: {self.file_path}")
            raise FileNotFoundError(f"IMD NetCDF file not found at: {self.file_path}")

        try:
            # Open NetCDF using xarray with netcdf4 engine
            self._dataset = xr.open_dataset(self.file_path, engine="netcdf4")
            self._lats = self._dataset["LATITUDE"].values
            self._lons = self._dataset["LONGITUDE"].values
            
            # Decode time variable to Python date objects
            raw_times = self._dataset["TIME"].values
            decoded_times = []
            for t in raw_times:
                if isinstance(t, np.datetime64):
                    dt = pd.to_datetime(t)
                    decoded_times.append(dt.date())
                elif hasattr(t, "year"):  # cftime
                    decoded_times.append(date(t.year, t.month, t.day))
                else:
                    raise ValueError(f"Unsupported time coordinate format: {type(t)}")
            
            self._times = decoded_times
            logger.info(
                f"Successfully loaded NetCDF dataset: {self.file_path}. "
                f"Lats: {len(self._lats)}, Lons: {len(self._lons)}, Days: {len(self._times)}"
            )
        except Exception as e:
            logger.exception(f"Failed to initialize IMD NetCDF file: {e}")
            raise

    def get_coordinates(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns latitude and longitude grid coordinates.
        """
        if self._lats is None or self._lons is None:
            raise RuntimeError("Dataset is not initialized.")
        return self._lats, self._lons

    def get_time_dimension(self) -> List[date]:
        """
        Returns the list of dates in the time dimension.
        """
        if self._times is None:
            raise RuntimeError("Dataset is not initialized.")
        return self._times

    def get_rainfall(self, lat: float, lon: float, query_date: date) -> Optional[float]:
        """
        Retrieves the rainfall value (in mm) for a specific coordinate and date.
        If coordinate or date is out-of-bounds, returns None.
        If coordinate falls on missing value (coastal/sea), returns None.
        """
        if self._dataset is None or self._lats is None or self._lons is None or self._times is None:
            raise RuntimeError("Dataset is not initialized.")

        # Find closest grid indices
        lat_idx = int(np.abs(self._lats - lat).argmin())
        lon_idx = int(np.abs(self._lons - lon).argmin())

        # Check threshold to ensure query coordinates are within reasonable proximity of closest grid center
        if np.abs(self._lats[lat_idx] - lat) > 0.25 or np.abs(self._lons[lon_idx] - lon) > 0.25:
            logger.warning(f"Query coordinates ({lat}, {lon}) are out of grid bounds.")
            return None

        # Find matching date index
        try:
            time_idx = self._times.index(query_date)
        except ValueError:
            return None

        # Fetch rainfall value
        val = float(self._dataset["RAINFALL"][time_idx, lat_idx, lon_idx].values)
        
        # Handle nan / missing value indicators (-999.0)
        if np.isnan(val) or val == -999.0:
            return None

        return val

    def get_rainfall_observation(self, lat: float, lon: float, query_date: date) -> Optional[RainfallObservation]:
        """
        Retrieves a structured RainfallObservation object.
        """
        val = self.get_rainfall(lat, lon, query_date)
        if val is None:
            return None
        return RainfallObservation(
            date=query_date,
            latitude=float(lat),
            longitude=float(lon),
            rainfall_mm=val
        )

    def close(self):
        """
        Closes the dataset resource.
        """
        if self._dataset is not None:
            self._dataset.close()
