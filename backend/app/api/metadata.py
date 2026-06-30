"""
Metadata API Router.

Purpose:
    Exposes endpoints for retrieving catalog structures of administrative boundaries
    (states, districts) and meteorological parameters.
"""

from typing import Optional
from fastapi import APIRouter, Query, status, HTTPException
from app.schemas import MetadataResponse

router = APIRouter()


@router.get(
    "/states",
    response_model=MetadataResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="List Supported Indian States",
    description="Returns a complete list of administrative Indian States supported by the digital twin platform.",
)
async def get_states():
    """
    Retrieves supported states. Returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Metadata repository service is not implemented."
    )


@router.get(
    "/districts",
    response_model=MetadataResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="List Supported Districts",
    description="Returns a list of districts supported by the digital twin, with optional state-level filtering.",
)
async def get_districts(
    state: Optional[str] = Query(
        None,
        min_length=2,
        description="Optional state filter to restrict returned districts (e.g. 'Maharashtra')"
    )
):
    """
    Retrieves supported districts. Returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Metadata repository service is not implemented."
    )


@router.get(
    "/parameters",
    response_model=MetadataResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="List Supported Climate Parameters",
    description="Returns a list of all climate parameters/variables currently measured or modeled by the digital twin.",
)
async def get_parameters():
    """
    Retrieves supported climate parameters. Returns HTTP 501 (Not Implemented) for Sprint 2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Metadata repository service is not implemented."
    )
