"""
FastAPI Main Application Entry Point.

Purpose:
    This module initializes the FastAPI application instance, registers core middleware
    (like CORS), registers API routers, configures custom exception handlers, and manages
    the application lifespan (startup and shutdown logic).

Future Responsibilities:
    * Initialize connection pools to databases and Redis cache on startup.
    * Release socket connections and dump telemetry metrics on shutdown.
    * Warm up and pre-load PyTorch/ONNX ML models in the lifespan context.

TODO:
    * Integrate database session creation in application lifespan.
    * Add automated cache warmup sequences on startup.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config.settings import settings
from app.api.router import api_router
from app.exceptions.handlers import register_exception_handlers
import app.utils.logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous lifespan manager handling startup and shutdown operations.
    """
    # ----------------------------------------
    # Startup Sequence
    # ----------------------------------------
    logger.info(f"Starting {settings.APP_NAME} in environment: {settings.ENV}...")
    
    # Ensure local directory paths exist
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.MODEL_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Validated data and model directory structures.")
    
    yield  # Application runs here
    
    # ----------------------------------------
    # Shutdown Sequence
    # ----------------------------------------
    logger.info(f"Shutting down {settings.APP_NAME}...")
    logger.info("Lifespan resources released.")


# Initialize FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Digital Twin platform for modeling historical climate changes and predicting disaster scenarios across India.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENV != "prod" else None,
    redoc_url="/redoc" if settings.ENV != "prod" else None,
)

# CORS (Cross-Origin Resource Sharing) configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers registration
register_exception_handlers(app)

# Router Registration
app.include_router(api_router, prefix=settings.API_V1_STR)


# Direct health check endpoint at root level
@app.get("/health", tags=["System Health"], status_code=status.HTTP_200_OK)
async def get_health():
    """
    Direct health check endpoint.
    
    Returns:
        JSON response with the service health status.
    """
    return {
        "status": "healthy",
        "service": "PRITHVI Backend",
        "version": app.version
    }


# Root/Index Direct Health Redirect
@app.get("/", tags=["Root"], status_code=status.HTTP_200_OK)
async def read_root():
    """
    Root entry point.
    
    Returns basic application status metadata.
    """
    return {
        "app": settings.APP_NAME,
        "environment": settings.ENV,
        "version": app.version,
        "status": "online"
    }

