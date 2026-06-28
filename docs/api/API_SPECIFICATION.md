# Project PRITHVI Backend API Specification

This document defines the REST API contracts for Sprint 2 of Project PRITHVI. These interfaces are designed to allow frontend and machine learning (ML) teams to integrate and develop in parallel.

---

## Global API Design Guidelines

### Base URL & Versioning
All endpoints, except the root health endpoint, are versioned and prefixed with:
`/api/v1`

### Standard Response Envelope
All success responses return a JSON object containing a `status` indicator set to `"success"`.
```json
{
  "status": "success",
  "message": "Operation completed successfully.",
  "data": { ... }
}
```

### Standard Error Envelope
All error responses (e.g. 400, 422, 500, 501) return a JSON object with `status` set to `"error"`, including a UTC timestamp and an optional details array indicating validation failures.
```json
{
  "status": "error",
  "message": "Validation failed.",
  "timestamp": "2026-06-28T03:14:15Z",
  "errors": [
    {
      "loc": ["query", "start_date"],
      "msg": "start_date must be before or equal to end_date",
      "type": "value_error"
    }
  ]
}
```

### Enums
- **ClimateParameter**: Defines the supported weather variables. Allowed values:
  - `"Temperature"`
  - `"Rainfall"`
  - `"LST"` (Land Surface Temperature)
  - `"SST"` (Sea Surface Temperature)

---

## Endpoint Specification

### 1. System Health

#### `GET /health`
* **Purpose**: Validate container and system availability (root level).
* **Response Status**: `200 OK`
* **Response Payload (`CommonResponse`)**:
  ```json
  {
    "status": "healthy",
    "service": "PRITHVI Backend",
    "version": "0.1.0"
  }
  ```

#### `GET /api/v1/health`
* **Purpose**: Check versioned API status.
* **Response Status**: `200 OK`
* **Response Payload (`CommonResponse`)**:
  ```json
  {
    "status": "healthy",
    "service": "PRITHVI Backend",
    "version": "0.1.0"
  }
  ```

---

### 2. Climate Resource Hierarchy

#### `GET /api/v1/climate/history`
* **Purpose**: Retrieve historical observation timeline for selected climate parameters.
* **Query Parameters**:
  - `state` (string, required): Name of the Indian State (min length 2).
  - `district` (string, required): Name of the district (min length 2).
  - `start_date` (date, YYYY-MM-DD, required): Start date.
  - `end_date` (date, YYYY-MM-DD, required): End date. Must be on or after `start_date`.
  - `variables` (List of `ClimateParameter` enums, required): Parameters to retrieve.
* **Response Status**: `501 Not Implemented` (Sprint 2 contract stub)
* **Target Success Response Model (`ClimateHistoryResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Historical climate data retrieved successfully.",
    "state": "Maharashtra",
    "district": "Pune",
    "start_date": "2023-01-01",
    "end_date": "2023-01-02",
    "data": [
      {
        "date": "2023-01-01",
        "Temperature": 24.5,
        "Rainfall": 0.0
      },
      {
        "date": "2023-01-02",
        "Temperature": 23.8,
        "Rainfall": 1.2
      }
    ]
  }
  ```

#### `GET /api/v1/climate/current`
* **Purpose**: Get near real-time observed parameters for a district.
* **Query Parameters**:
  - `state` (string, required): Name of the State.
  - `district` (string, required): Name of the district.
  - `variables` (List of `ClimateParameter` enums, required): Parameters to retrieve.
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`CommonResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Current observations retrieved successfully.",
    "data": {
      "state": "Maharashtra",
      "district": "Pune",
      "timestamp": "2026-06-28T08:00:00Z",
      "Temperature": 28.5,
      "Rainfall": 0.0
    }
  }
  ```

#### `GET /api/v1/climate/overview`
* **Purpose**: Fetch a lightweight, aggregated district summary dashboard feed in a single request.
* **Query Parameters**:
  - `state` (string, required): Name of the State.
  - `district` (string, required): Name of the district.
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`ClimateOverviewResponse`)**:
  ```json
  {
    "status": "success",
    "message": "District overview summary dashboard compiled.",
    "state": "Maharashtra",
    "district": "Pune",
    "metrics": {
      "Temperature": {"value": 29.4, "unit": "°C"},
      "Rainfall": {"value": 12.0, "unit": "mm"},
      "LST": {"value": 31.2, "unit": "°C"}
    },
    "recent_anomalies": [
      {
        "date": "2026-06-20",
        "parameter": "Rainfall",
        "severity": "High",
        "description": "Rainfall exceeded 95th percentile threshold by 45%."
      }
    ],
    "forecast_summary": {
      "status": "Normal",
      "next_7_days_risk": "Low",
      "weather_warning": null
    }
  }
  ```

#### `GET /api/v1/climate/predictions`
* **Purpose**: Retrieve ML-based climate forecasts.
* **Query Parameters**:
  - `state` (string, required): Name of the State.
  - `district` (string, required): Name of the district.
  - `horizon_days` (integer, required): Days to forecast (1 to 365).
  - `variables` (List of `ClimateParameter` enums, required): Target variables to forecast.
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`PredictionResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Weather forecast generated successfully.",
    "state": "Maharashtra",
    "district": "Pune",
    "horizon_days": 7,
    "predictions": [
      {
        "date": "2026-06-29",
        "Temperature": {
          "mean": 28.5,
          "upper": 30.1,
          "lower": 26.9
        },
        "Rainfall": {
          "mean": 12.4,
          "upper": 18.0,
          "lower": 8.1
        }
      }
    ]
  }
  ```

#### `POST /api/v1/climate/simulate`
* **Purpose**: Trigger a simulated climate anomaly or disaster scenario.
* **Request Body (`SimulationRequest`)**:
  ```json
  {
    "scenario_type": "extreme_rainfall",
    "state": "Maharashtra",
    "district": "Pune",
    "intensity_multiplier": 1.5,
    "duration_days": 5,
    "additional_params": {
      "initial_reservoir_capacity": 0.85
    }
  }
  ```
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`SimulationResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Simulation run completed successfully.",
    "simulation_id": "sim_8f99ad92-12fc-4b53-9092-2df5e8c1482e",
    "scenario_type": "extreme_rainfall",
    "metrics": {
      "peak_rainfall_multiplier": 1.5,
      "max_daily_rainfall_mm": 185.2,
      "estimated_flood_risk": "High"
    },
    "timeline": [
      {
        "day": 1,
        "simulated_rainfall_mm": 45.0,
        "flooded_area_sq_km": 0.0
      },
      {
        "day": 2,
        "simulated_rainfall_mm": 185.2,
        "flooded_area_sq_km": 1.4
      }
    ]
  }
  ```

---

### 3. Metadata Resource Hierarchy

#### `GET /api/v1/metadata/states`
* **Purpose**: List supported states in the application.
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`MetadataResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Supported states retrieved.",
    "count": 3,
    "items": ["Maharashtra", "Karnataka", "Tamil Nadu"]
  }
  ```

#### `GET /api/v1/metadata/districts`
* **Purpose**: List supported districts, optionally filtered by state.
* **Query Parameters**:
  - `state` (string, optional): State name to filter districts.
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`MetadataResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Supported districts retrieved.",
    "count": 2,
    "items": ["Pune", "Mumbai City"]
  }
  ```

#### `GET /api/v1/metadata/parameters`
* **Purpose**: List supported climate parameters/variables.
* **Response Status**: `501 Not Implemented`
* **Target Success Response Model (`MetadataResponse`)**:
  ```json
  {
    "status": "success",
    "message": "Supported climate parameters retrieved.",
    "count": 4,
    "items": [
      {
        "name": "Temperature",
        "unit": "°C",
        "description": "Ambient atmospheric temperature"
      },
      {
        "name": "Rainfall",
        "unit": "mm",
        "description": "Daily accumulated precipitation"
      },
      {
        "name": "LST",
        "unit": "°C",
        "description": "Land Surface Temperature"
      },
      {
        "name": "SST",
        "unit": "°C",
        "description": "Sea Surface Temperature"
      }
    ]
  }
  ```
