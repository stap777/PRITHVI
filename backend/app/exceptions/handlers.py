"""
Custom Exceptions and Global Exception Handlers.

Purpose:
    Defines domain-specific exceptions for the Climate Digital Twin,
    and provides middleware-like handlers to catch and map these errors to standardized
    REST API responses.
"""

from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger


# ==============================================================================
# Domain-Specific Exception Definitions
# ==============================================================================
class ClimateTwinError(Exception):
    """Base exception class for all custom domain errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class GeospatialDataError(ClimateTwinError):
    """Raised when file reading, validation, or spatial transformations fail."""
    pass


class ModelLoadError(ClimateTwinError):
    """Raised when ML model weights cannot be loaded, signature fails, or missing."""
    pass


class SimulationError(ClimateTwinError):
    """Raised when simulation parameters are invalid, or math models diverge."""
    pass


class DistrictNotFoundError(ClimateTwinError):
    """Raised when the requested state/district combination does not exist in the catalog."""
    pass


# ==============================================================================
# Global Exception Registration
# ==============================================================================
def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers custom exception handlers on the FastAPI application instance.
    
    Args:
        app: The target FastAPI application instance.
    """
    
    @app.exception_handler(DistrictNotFoundError)
    async def district_not_found_exception_handler(request: Request, exc: DistrictNotFoundError) -> JSONResponse:
        logger.error(f"District Not Found: {exc.message} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "message": exc.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "errors": [exc.details] if exc.details else None
            }
        )

    @app.exception_handler(ClimateTwinError)
    async def climate_twin_exception_handler(request: Request, exc: ClimateTwinError) -> JSONResponse:
        logger.error(f"Domain Error: {exc.message} | Details: {exc.details} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "message": exc.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "errors": [exc.details] if exc.details else None
            }
        )

    @app.exception_handler(GeospatialDataError)
    async def geospatial_exception_handler(request: Request, exc: GeospatialDataError) -> JSONResponse:
        logger.error(f"Geospatial Error: {exc.message} | Details: {exc.details}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": exc.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "errors": [exc.details] if exc.details else None
            }
        )

    @app.exception_handler(ModelLoadError)
    async def model_load_exception_handler(request: Request, exc: ModelLoadError) -> JSONResponse:
        logger.error(f"Model Load Error: {exc.message} | Details: {exc.details}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "message": exc.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "errors": [exc.details] if exc.details else None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = []
        for err in exc.errors():
            errors.append({
                "loc": [str(x) for x in err["loc"]],
                "msg": err["msg"],
                "type": err["type"]
            })
        logger.warning(f"Request Validation Failure: {errors} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": "Validation failed.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "errors": errors
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(f"Unhandled Global Exception: {str(exc)} at path {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "An unexpected server-side error occurred. Please try again later.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "errors": None
            }
        )
