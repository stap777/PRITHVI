"""
Custom Exceptions and Global Exception Handlers.

This module defines domain-specific exceptions for the Climate Digital Twin,
and provides middleware-like handlers to catch and map these errors to standardized
REST API responses.

Classes:
    ClimateTwinError: Base exception for all custom domain errors.
    GeospatialDataError: Raised when parsing/finding raster or vector data fails.
    ModelLoadError: Raised when ML model file retrieval or loading fails.
    SimulationError: Raised when numerical simulations run out of bounds or fail.

Functions:
    register_exception_handlers: Configures exception handlers on a FastAPI instance.

TODO:
    * Integrate error alert/telemetry forwarding (e.g., Sentry).
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
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


# ==============================================================================
# Global Exception Registration
# ==============================================================================
def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers custom exception handlers on the FastAPI application instance.
    
    Args:
        app: The target FastAPI application instance.
    """
    
    @app.exception_handler(ClimateTwinError)
    async def climate_twin_exception_handler(request: Request, exc: ClimateTwinError) -> JSONResponse:
        logger.error(f"Domain Error: {exc.message} | Details: {exc.details} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(GeospatialDataError)
    async def geospatial_exception_handler(request: Request, exc: GeospatialDataError) -> JSONResponse:
        logger.error(f"Geospatial Error: {exc.message} | Details: {exc.details}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "GEOSPATIAL_VALIDATION_ERROR",
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(ModelLoadError)
    async def model_load_exception_handler(request: Request, exc: ModelLoadError) -> JSONResponse:
        logger.error(f"Model Load Error: {exc.message} | Details: {exc.details}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "success": False,
                "error": {
                    "code": "ML_MODEL_ERROR",
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(f"Unhandled Global Exception: {str(exc)} at path {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server-side error occurred. Please try again later.",
                    "details": {}
                }
            }
        )
