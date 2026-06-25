"""
Geospatial Vector Utilities.

This module provides helpers for vector geometries, coordinate reference systems (CRS)
transformations, and geographical boundary validations.

Functions:
    is_within_india: Verifies if a lat/lon coordinate falls within standard boundaries.
    reproject_geometry: Transforms geometry coordinates between reference systems.
    geojson_to_shape: Parses a raw GeoJSON dictionary into a Shapely geometry object.

TODO:
    * Integrate fiona or shapely validation error handlers.
"""

from typing import Dict, Any, Tuple
from shapely.geometry import shape, BaseGeometry
import geopandas as gpd
from loguru import logger

from app.config.constants import INDIA_BOUNDING_BOX, EPSG_WGS84, EPSG_INDIA_ALBERS


def is_within_india(lat: float, lon: float) -> bool:
    """
    Validates if coordinate falls inside the Indian subcontinent bounding box.
    
    Args:
        lat: Latitude decimal value.
        lon: Longitude decimal value.
    """
    min_lon, min_lat, max_lon, max_lat = INDIA_BOUNDING_BOX
    within_bbox = min_lon <= lon <= max_lon and min_lat <= lat <= max_lat
    
    logger.debug(f"Coordinate validation ({lat}, {lon}): inside_bbox={within_bbox}")
    return within_bbox


def reproject_geometry(
    geom_dict: Dict[str, Any],
    source_crs: str = EPSG_WGS84,
    target_crs: str = EPSG_INDIA_ALBERS
) -> BaseGeometry:
    """
    Reprojects GeoJSON dictionary geometry coordinates to target CRS.
    
    Args:
        geom_dict: Input GeoJSON coordinate dictionary.
        source_crs: CRS of input geometry (default EPSG:4326).
        target_crs: Destination target CRS (default EPSG:7755).
        
    Returns:
        Reprojected Shapely geometry.
    """
    logger.info(f"Reprojecting geometry from {source_crs} to {target_crs}")
    
    # In production, we construct GeoDataFrame and reproject:
    # geom = shape(geom_dict)
    # gdf = gpd.GeoDataFrame(index=[0], crs=source_crs, geometry=[geom])
    # gdf_reprojected = gdf.to_crs(target_crs)
    # return gdf_reprojected.geometry.iloc[0]

    # Mock return shape
    logger.warning("Reproject geometry mock executed.")
    return shape(geom_dict)


def geojson_to_shape(geom_dict: Dict[str, Any]) -> BaseGeometry:
    """
    Loads raw GeoJSON coordinates dictionary into a shapely spatial geometry.
    """
    try:
        return shape(geom_dict)
    except Exception as e:
        logger.error(f"Failed to parse GeoJSON dictionary: {str(e)}")
        raise ValueError("Invalid GeoJSON geometry representation provided.") from e
