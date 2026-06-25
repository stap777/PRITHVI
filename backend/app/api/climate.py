"""
Climate Core Data Router.

This controller exposes REST API endpoints for querying historical meteorological 
timeseries datasets, reading geospatial raster metadata, and applying boundary mask
clips to environmental grids.

Attributes:
    router: Climate endpoints router instance.

TODO:
    * Connect database session dependency injections.
    * Implement file streaming for large raster TIFF results.
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status

from app.schemas.climate import (
    HistoricalClimateQuery,
    HistoricalClimateResponse,
    RasterMetadataResponse,
    RasterClipRequest,
    RasterClipResponse
)
from app.services.climate_service import ClimateService

router = APIRouter()


# Dependency provider for Climate Service
def get_climate_service() -> ClimateService:
    """Dependency injection provider for Climate Business Service."""
    return ClimateService()


@router.get(
    "/history",
    response_model=HistoricalClimateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Historical Climate Records",
    description="Retrieve gridded temperature and rainfall data from IMD observations.",
)
async def get_historical_climate(
    lat: float = Query(..., ge=6.0, le=36.0, description="Latitude (India bounds)"),
    lon: float = Query(..., ge=68.0, le=98.0, description="Longitude (India bounds)"),
    start_year: int = Query(1980, ge=1901, le=2024),
    end_year: int = Query(2020, ge=1901, le=2024),
    params: List[str] = Query(["temperature", "rainfall"]),
    service: ClimateService = Depends(get_climate_service)
):
    """
    Retrieves historical meteorological datasets using coordinates and year ranges.
    """
    query = HistoricalClimateQuery(
        latitude=lat,
        longitude=lon,
        start_year=start_year,
        end_year=end_year,
        parameters=params
    )
    # The service returns placeholder/mock data conforming to response schema
    return service.get_historical_records(query)


@router.get(
    "/raster/metadata",
    response_model=RasterMetadataResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Raster Metadata",
    description="Extract coordinates extent, bands, and resolution of an environmental raster.",
)
async def get_raster_metadata(
    filename: str = Query(..., description="Target file name in data storage"),
    service: ClimateService = Depends(get_climate_service)
):
    """
    Exposes structural header metadata of NetCDF or GeoTIFF files.
    """
    return service.get_raster_file_info(filename)


@router.post(
    "/raster/clip",
    response_model=RasterClipResponse,
    status_code=status.HTTP_200_OK,
    summary="Clip Raster to Boundary",
    description="Calculate stats (mean, min, max) for a specific raster inside a GeoJSON polygon mask.",
)
async def clip_raster_boundary(
    request: RasterClipRequest,
    service: ClimateService = Depends(get_climate_service)
):
    """
    Clips and processes spatial grids using a vector polygon boundary mask.
    """
    return service.process_raster_clip(request)
