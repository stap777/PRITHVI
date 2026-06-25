"""
Application Configuration Settings.

This module defines the Pydantic Settings class to manage environment variables 
for the Climate Digital Twin Backend. It leverages pydantic-settings to validate
types and load defaults.

Classes:
    Settings: Global application configuration class.

TODO:
    * Set up secret management integrations for AWS Secrets Manager or Vault if deployed to cloud.
    * Expand database connection strings once DB flavor is chosen.
"""

from typing import List, Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    
    Attributes:
        APP_NAME: Title of the FastAPI application.
        ENV: Application environment (dev, staging, prod).
        DEBUG: Boolean flag to enable traceback and debug levels.
        API_V1_STR: Prefix for Version 1 of the REST API.
        CORS_ORIGINS: List of allowed origins for cross-origin requests.
        
        DATA_DIR: Root directory containing NetCDF, GeoTIFF, and GeoJSON files.
        MODEL_DIR: Directory where pre-trained ML model weight artifacts are located.
        
        REDIS_URL: Redis server connection URL (caching).
        CACHE_TTL_SECONDS: Default expiration duration for cached items.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Core API Config
    APP_NAME: str = "Climate Digital Twin of India"
    ENV: str = Field(default="dev", description="Environment stage: dev, test, prod")
    DEBUG: bool = Field(default=True, description="Enable debug level outputs")
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )

    # Storage Paths
    DATA_DIR: Path = Field(
        default=Path("data"), 
        description="Root directory for geospatial data structures"
    )
    MODEL_DIR: Path = Field(
        default=Path("models"), 
        description="Root directory storing PyTorch / ONNX / XGBoost models"
    )

    # Cache & Services
    REDIS_URL: Optional[str] = Field(
        default="redis://localhost:6379/0", 
        description="Cache database endpoint connection string"
    )
    CACHE_TTL_SECONDS: int = Field(
        default=3600, 
        description="Default Cache Time-To-Live in seconds"
    )

    @property
    def imd_data_dir(self) -> Path:
        """Helper to get IMD data sub-directory."""
        return self.DATA_DIR / "imd"

    @property
    def insat_data_dir(self) -> Path:
        """Helper to get INSAT data sub-directory."""
        return self.DATA_DIR / "insat"


# Instantiate a singleton config loader
settings = Settings()
