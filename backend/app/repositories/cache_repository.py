"""
Cache Repository Wrapper.

This module provides a caching abstraction layer utilizing Redis, with a fallback
to an in-memory dictionary if Redis is unavailable. This is critical for storing
heavy spatial statistics computations.

Classes:
    CacheRepository: Caching adapter interface.

TODO:
    * Connect actual redis.asyncio client connection pooling.
"""

from typing import Any, Optional
from loguru import logger

from app.config.settings import settings


class CacheRepository:
    """
    Caching adapter offering key-value lookups with automatic TTL options.
    """

    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self._in_memory_fallback = {}
        logger.info("Initializing CacheRepository.")
        if not self.redis_url:
            logger.warning("Redis URL not provided; falling back to temporary local dictionary cache.")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves serialized data from cache store.
        """
        logger.debug(f"Cache lookup for key: {key}")
        # In production, self.redis.get(key)
        return self._in_memory_fallback.get(key)

    def set(self, key: str, value: Any, ttl_seconds: int = None) -> bool:
        """
        Stores data inside cache.
        """
        ttl = ttl_seconds or settings.CACHE_TTL_SECONDS
        logger.debug(f"Caching key: {key} (TTL: {ttl}s)")
        
        # In production, self.redis.setex(key, ttl, value)
        self._in_memory_fallback[key] = value
        return True

    def delete(self, key: str) -> bool:
        """
        Clears key from cache.
        """
        logger.debug(f"Evicting cache key: {key}")
        if key in self._in_memory_fallback:
            del self._in_memory_fallback[key]
            return True
        return False
