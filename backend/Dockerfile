# ==============================================================================
# Stage 1: Build & Dependencies
# ==============================================================================
FROM python:3.12-slim-bookworm AS builder

# Set shell and environment variables
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install system-level build tools and geospatial libraries (GDAL, PROJ, GEOS)
# required for compiling dependencies like rasterio and shapely if needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies into a local directory
COPY requirements.txt .
RUN pip install --target=/build/dependencies -r requirements.txt

# ==============================================================================
# Stage 2: Final Runtime Image
# ==============================================================================
FROM python:3.12-slim-bookworm AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install runtime dependencies for geospatial operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal32 \
    libproj25 \
    libgeos-c1v5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /build/dependencies /usr/local/lib/python3.12/site-packages
COPY --from=builder /build/dependencies/bin /usr/local/bin

# Copy app code
COPY app /app/app

# Change ownership of application directories
RUN mkdir -p /app/data /app/models /app/logs && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check using curl
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
