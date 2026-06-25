"""
Central API Router.

This module aggregates individual route controllers (health, climate, prediction,
and simulation) and exposes them through a single master router with appropriate tags
and prefixes.

Attributes:
    api_router: Central APIRouter instance to be registered in main.py.

TODO:
    * Set up API authentication and rate-limiting dependencies at this router level.
"""

from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.climate import router as climate_router
from app.api.prediction import router as prediction_router
from app.api.simulation import router as simulation_router

api_router = APIRouter()

# Register endpoint controllers
api_router.include_router(health_router, prefix="/health", tags=["System Health"])
api_router.include_router(climate_router, prefix="/climate", tags=["Climate Core Data"])
api_router.include_router(prediction_router, prefix="/prediction", tags=["AI Climate Prediction"])
api_router.include_router(simulation_router, prefix="/simulation", tags=["Climate Digital Twin Simulation"])
