"""
Climate Geospatial Schemas.

This module defines Pydantic validation models for historical climate queries,
spatial coordinates, bounding boxes, and raster file metadata.

Classes:
    Coordinates: Latitude and longitude point model.
    HistoricalClimateQuery: Input parameters for querying climate grids.
    ClimateDataPoint: A single temporal snapshot value of temperature and rainfall.
    HistoricalClimateResponse: Time-series of climate measurements.
    RasterMetadataResponse: Details of a GIS GeoTIFF raster file.
    RasterClipRequest: GeoJSON boundary parameters to clip grids.
    RasterClipResponse: Calculated statistics inside a clipped boundary.

TODO:
    * Support multiple meteorological parameters query dynamically.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class Coordinates(BaseModel):
    """Latitude and Longitude representation with standard range validations."""
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")


class HistoricalClimateQuery(BaseModel):
    """Query parameters to retrieve historical gridded temperature and precipitation."""
    latitude: float = Field(..., ge=6.0, le=36.0, description="Latitude constraint (within India bounds)")
    longitude: float = Field(..., ge=68.0, le=98.0, description="Longitude constraint (within India bounds)")
    start_year: int = Field(default=1980, ge=1901, le=2024, description="Inclusive start year")
    end_year: int = Field(default=2020, ge=1901, le=2024, description="Inclusive end year")
    parameters: List[str] = Field(
        default=["temperature", "rainfall"],
        description="Meteorological parameters to extract (e.g. temperature, rainfall, humidity)"
    )

    @field_validator("end_year")
    @classmethod
    def validate_year_range(cls, v: int, info) -> int:
        """Validates that start_year is less than or equal to end_year."""
        if "start_year" in info.data and v < info.data["start_year"]:
            raise ValueError("end_year must be greater than or equal to start_year")
        return v


class ClimateDataPoint(BaseModel):
    """Representing a single observation value at a specific timestamp."""
    year: int = Field(..., description="Observation year")
    month: int = Field(..., ge=1, le=12, description="Observation month")
    temperature: Optional[float] = Field(None, description="Average temperature in Celsius")
    rainfall: Optional[float] = Field(None, description="Accumulated rainfall in mm")


class HistoricalClimateResponse(BaseModel):
    """Historical climate response containing query info and matching timeseries data."""
    latitude: float
    longitude: float
    start_year: int
    end_year: int
    data: List[ClimateDataPoint] = Field(default=[], description="Timeseries list of observations")


class RasterMetadataResponse(BaseModel):
    """Structural details of a spatial raster file (NetCDF/GeoTIFF)."""
    filename: str = Field(..., description="Raster file name")
    crs: str = Field(..., description="Coordinate reference system (e.g. EPSG:4326)")
    width: int = Field(..., description="Grid width in cells")
    height: int = Field(..., description="Grid height in cells")
    bands: int = Field(..., description="Number of stacked channels/bands")
    bounds: List[float] = Field(..., description="Bounding box extent: [min_lon, min_lat, max_lon, max_lat]")
    resolution: List[float] = Field(..., description="Spatial grid cell resolution [x_res, y_res]")


class RasterClipRequest(BaseModel):
    """Request params for clipping a raster using standard GeoJSON polygons."""
    raster_name: str = Field(..., description="Identified filename of the raster")
    geometry: Dict[str, Any] = Field(
        ...,
        description="Standard GeoJSON Geometry dictionary representing the polygon region"
    )


class RasterClipResponse(BaseModel):
    """Spatial statistics calculated over a clipped raster polygon."""
    raster_name: str
    mean_val: float = Field(..., description="Average value across cells in clipped area")
    min_val: float = Field(..., description="Minimum cell value")
    max_val: float = Field(..., description="Maximum cell value")
    std_dev: float = Field(..., description="Standard deviation")
    nodata_count: int = Field(..., description="Number of pixels with NoData values in clip mask")
