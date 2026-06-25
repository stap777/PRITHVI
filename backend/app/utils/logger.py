"""
Structured Logging Configuration.

This module configures the Loguru logger to output formatted logs to stdout 
and rotating log files on disk.

TODO:
    * Integrate logging forwarder to standard JSON formats for cloud aggregators.
"""

import sys
from pathlib import Path
from loguru import logger

from app.config.settings import settings

# Setup standard formatting
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def configure_logging() -> None:
    """
    Configures Loguru logging sink parameters.
    """
    # Remove default handler
    logger.remove()

    # Determine logging level based on debug setting
    log_level = "DEBUG" if settings.DEBUG else "INFO"

    # Add console sink
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=log_level,
        colorize=True
    )

    # Add rotating log file sink
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "backend_server.log",
        format=LOG_FORMAT,
        level="INFO",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    
    logger.info(f"Structured logging initialized at level: {log_level}")


# Run configuration upon import
configure_logging()
