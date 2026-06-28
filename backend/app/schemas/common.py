"""
Common API schemas for standardizing success and error response shapes.

Purpose:
    Ensures that all API response structures adhere to a unified interface design.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class CommonResponse(BaseModel):
    """
    Standard top-level envelope for successful API operations.
    """
    status: Literal["success", "error"] = Field(
        default="success",
        description="Outcome category: 'success' for successful operations or 'error' for failed ones."
    )
    message: str = Field(
        ...,
        description="Human-readable explanation of the operational outcome."
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional payload dictionary containing requested entities or key-value structures."
    )


class ErrorResponse(BaseModel):
    """
    Standardized payload for error responses (e.g. 400, 422, 500, 501).
    """
    status: Literal["error"] = Field(
        default="error",
        description="Always 'error' for failure envelopes."
    )
    message: str = Field(
        ...,
        description="General description of the error."
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="ISO 8601 formatted UTC timestamp representing when the error occurred."
    )
    errors: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Granular error details, typically mapping to input field validation location and messages."
    )
