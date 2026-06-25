"""
FastAPI Main Application Entry Point.

This module initializes the FastAPI application instance, registers core middleware
(like CORS), registers API routers, configures custom exception handlers, and manages
the application lifespan (startup and shutdown logic).

TODO:
    * Set up database connection pool inside the lifespan event.
    * Warm up ML models on startup.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config.settings import settings
from app.api.router import api_router
from app.exceptions.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous lifespan manager handling startup and shutdown operations.
    
    Operations:
        - Startup: Verify config settings, check directory structure, pre-load ML model signatures.
        - Shutdown: Release DB connections, close network clients, clear active thread pools.
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
    version="1.0.0",
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
