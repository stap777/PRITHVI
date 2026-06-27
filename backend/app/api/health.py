"""
System Health Router.

Purpose:
    This module provides endpoints for monitoring application status and validating
    the availability of the PRITHVI backend service.

Future Responsibilities:
    * Perform active health checks on downstream infrastructure (e.g. database, Redis, S3).
    * Monitor disk usage of the local raster cache directory.
    * Check if ML model weights are loaded and the inference server is responsive.

TODO:
    * Implement health check integrations for Redis and database connection pools.
    * Add custom system resource monitoring (memory, CPU, disk IO).
"""

from fastapi import APIRouter, status
from loguru import logger

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get Service Status",
    description="Validates the status of the PRITHVI Backend service.",
)
async def check_health():
    """
    Evaluates system status and returns the service metadata.
    
    Returns:
        JSON response with the service health status.
    """
    logger.info("Executing health check endpoint.")
    return {
        "status": "healthy",
        "service": "PRITHVI Backend",
        "version": "0.1.0"
    }

