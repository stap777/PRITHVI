"""
Enums definitions for the PRITHVI backend schemas.

Purpose:
    Provides centralized, validated string enums for various query and request fields.
"""

from enum import Enum


class ClimateParameter(str, Enum):
    """
    Supported climate parameters for history, prediction, and simulation endpoints.
    """
    TEMPERATURE = "Temperature"
    RAINFALL = "Rainfall"
    LST = "LST"
    SST = "SST"
