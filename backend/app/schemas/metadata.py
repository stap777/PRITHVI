"""
Metadata-related schemas for the PRITHVI backend API.

Purpose:
    Defines response structures for querying administrative areas (states, districts) and parameters list.
"""

from typing import Any, List, Literal
from pydantic import BaseModel, Field


class MetadataResponse(BaseModel):
    """
    Standardized payload wrapping list-based metadata responses.
    """
    status: Literal["success"] = Field(
        default="success",
        description="Always 'success' for successful responses."
    )
    message: str = Field(
        ...,
        description="Summary description of the retrieved metadata."
    )
    count: int = Field(
        ...,
        ge=0,
        description="The number of items returned in the list."
    )
    items: List[Any] = Field(
        ...,
        description="List of metadata items (could be simple strings or rich dictionaries)."
    )
