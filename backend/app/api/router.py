"""
Central API Router.

This module aggregates individual route controllers and exposes them through a single master router.

Attributes:
    api_router: Central APIRouter instance to be registered in main.py.
"""

from fastapi import APIRouter

from app.api.health import router as health_router

api_router = APIRouter()

# Register endpoint controllers
api_router.include_router(health_router, prefix="/health", tags=["System Health"])

