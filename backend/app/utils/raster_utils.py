"""
Geospatial Raster Utilities.

This module provides helper utilities for opening, downscaling, and clipping 
geographic raster grids (GeoTIFF / NetCDF datasets).

Functions:
    extract_point_from_raster: Extracts meteorological value matching coordinate.
    clip_raster_by_polygon: Cuts and masks raster cells using a vector boundary.

TODO:
    * Integrate rasterio.mask to crop TIFF files on coordinate masks.
    * Implement spatial interpolation (Bilinear/Nearest Neighbor) for upscaling.
"""

from typing import List, Dict, Any, Tuple
from pathlib import Path
from shapely.geometry import BaseGeometry
import numpy as np
from loguru import logger


def extract_point_from_raster(
    raster_path: Path,
    lat: float,
    lon: float,
    band: int = 1
) -> float:
    """
    Looks up cell pixel value at coordinates.
    
    Args:
        raster_path: Local path to GeoTIFF or NetCDF grid.
        lat: Target latitude.
        lon: Target longitude.
        band: Stacked band layer index (usually month or year).
        
    Returns:
        Float value of matching grid pixel.
    """
    logger.info(f"Extracting point value from {raster_path.name} at ({lat}, {lon}) band {band}")
    
    # In production, we run:
    # with rasterio.open(raster_path) as src:
    #     # Transform lat/lon coordinates to raster pixel index coordinates
    #     row, col = src.index(lon, lat)
    #     # Read the cell band value
    #     val = src.read(band)[row, col]
    #     return float(val)

    # Return mock value (typical temperature anomaly)
    return 26.4


def clip_raster_by_polygon(
    raster_path: Path,
    polygon_geom: BaseGeometry
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Clips raster cells boundaries to intersect only inside a vector polygon.
    
    Args:
        raster_path: Local path to target raster file.
        polygon_geom: Boundary polygon shape.
        
    Returns:
        Tuple containing cropped raster grid array and updated affine transform metadata.
    """
    logger.info(f"Clipping raster: {raster_path.name} with shape bounding box: {polygon_geom.bounds}")

    # In production:
    # with rasterio.open(raster_path) as src:
    #     out_image, out_transform = rasterio.mask.mask(src, [polygon_geom], crop=True)
    #     out_meta = src.meta.copy()
    #     out_meta.update({"driver": "GTiff", "height": out_image.shape[1], ...})
    #     return out_image[0], out_meta
    
    # Return mock arrays (10x10 cell clipping result)
    dummy_grid = np.random.uniform(5.0, 50.0, (10, 10))
    dummy_transform = {"crs": "EPSG:4326", "transform": [0.25, 0.0, 68.0, 0.0, -0.25, 36.0]}
    
    return dummy_grid, dummy_transform
