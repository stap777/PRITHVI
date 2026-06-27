"""
Domain and Physical Constants.

Purpose:
    This module stores read-only constants used across the Climate Digital Twin platform,
    including physical calculations, geodetic boundaries, and default parameters.

Future Responsibilities:
    * Store physical constants for agricultural, hydrological, and meteorological models.
    * Maintain projection CRS mappings and geospatial boundary coordinate constants.

TODO:
    * Align coordinate limits with official Survey of India boundary parameters.
    * Expand agricultural crop coefficient arrays (Kc values) for regional crops.
"""

from typing import Dict, Tuple

# ==============================================================================
# 1. GEODETIC & REGIONAL BOUNDS (WGS84 EPSG:4326)
# ==============================================================================
# Bounding box for the Indian subcontinent: (Min Lon, Min Lat, Max Lon, Max Lat)
INDIA_BOUNDING_BOX: Tuple[float, float, float, float] = (68.1, 6.4, 97.4, 35.5)

# Coordinate projection EPSG identifiers
EPSG_WGS84: str = "EPSG:4326"       # standard latitude/longitude coordinates
EPSG_INDIA_ALBERS: str = "EPSG:7755" # Equal Area projection recommended for India mapping

# ==============================================================================
# 2. METEOROLOGICAL BASELINES & DEFAULTS
# ==============================================================================
HISTORICAL_BASELINE_START_YEAR: int = 1961
HISTORICAL_BASELINE_END_YEAR: int = 1990

# Standard meteorological physical thresholds
STANDARD_ATMOSPHERIC_PRESSURE_HPA: float = 1013.25
KELVIN_OFFSET: float = 273.15

# ==============================================================================
# 3. DISASTER AND RISK IMPACT INDEX PARAMETERS
# ==============================================================================
# Thresholds for extreme weather hazard events
FLOOD_HEAVY_RAINFALL_THRESHOLD_MM_HR: float = 50.0  # Precipitation rate triggering risk
DROUGHT_SPI_CRITICAL_THRESHOLD: float = -1.5        # SPI index indicating severe drought

# Crop stress indices parameters (baseline critical temperature thresholds in Celsius)
CROP_TEMPERATURE_THRESHOLDS: Dict[str, Dict[str, float]] = {
    "rice": {
        "min_optimal": 20.0,
        "max_optimal": 35.0,
        "critical_maximum": 40.0
    },
    "wheat": {
        "min_optimal": 15.0,
        "max_optimal": 25.0,
        "critical_maximum": 32.0
    },
    "maize": {
        "min_optimal": 18.0,
        "max_optimal": 32.0,
        "critical_maximum": 38.0
    }
}
