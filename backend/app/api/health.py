"""
System Health Router.

This module provides endpoints for monitoring application status and validating
the availability of critical system dependencies (databases, cache, raster files).

Attributes:
    router: Health check endpoint router instance.

TODO:
    * Connect actual Redis client check in health endpoint.
    * Check free disk space availability for temporary raster clips.
"""

from fastapi import APIRouter, status
from loguru import logger

from app.config.settings import settings

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get Service Status",
    description="Validates status of FastAPI service and its infrastructure dependencies.",
)
async def check_health():
    """
    Evaluates system status, verifying directories and cache availability.
    
    Returns:
        JSON response with detailed system checks.
    """
    logger.info("Running health check verification sequence...")
    
    # Placeholder checks for system directories
    data_dir_ok = settings.DATA_DIR.exists()
    model_dir_ok = settings.MODEL_DIR.exists()

    # Placeholder status for cache and model availability
    # In a full run, we would ping Redis and check loaded model signatures.
    redis_connected = True if settings.REDIS_URL else False
    models_warmed = True

    overall_status = "healthy"
    if not (data_dir_ok and model_dir_ok):
        overall_status = "degraded"
        logger.warning(
            f"Storage status degraded: Data Dir Exists={data_dir_ok}, Model Dir Exists={model_dir_ok}"
        )

    return {
        "status": overall_status,
        "environment": settings.ENV,
        "services": {
            "api_server": "online",
            "redis_cache": "connected" if redis_connected else "disabled",
            "local_raster_storage": "accessible" if data_dir_ok else "inaccessible",
            "ml_inference_warmed": "ready" if models_warmed else "not_loaded"
        },
        "details": {
            "data_directory": str(settings.DATA_DIR),
            "model_directory": str(settings.MODEL_DIR)
        }
    }
