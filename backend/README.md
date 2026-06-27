# PRITHVI Backend Service — Sprint 1 Bootstrap

PRITHVI (Prithvi Representational Index for Temporal Hazard Validation and Informatics) is an AI-powered Digital Twin platform of India's climate, developed for the Bharatiya Antariksh Hackathon.

This repository contains the bootstrapped foundation of the FastAPI backend service.

---

## 📢 Sprint 1 Boundaries & Architecture Stability

**IMPORTANT**: Sprint 1 establishes ONLY the backend foundation and infrastructure scaffolding.
* Core application entry point, environment configuration, structured logging, router registration, exception handler middleware, and the GET `/health` endpoint are functional.
* Future domain layers—such as Climate APIs, Prediction APIs, Simulation APIs, ML model loaders, repositories, and business services—are not implemented in this sprint.
* To keep the project structure stable, empty placeholder directories (`app/services/`, `app/repositories/`, `app/schemas/`, `app/ml/`, and `app/simulation/`) are retained with Python package initializers (`__init__.py`). These will be implemented incrementally in later sprints.

```
backend/
├── app/                        # Main application core package
│   ├── api/                    # API Controller layer (Endpoints & Routing)
│   │   ├── router.py           # Master router registering sub-modules
│   │   └── health.py           # Health check endpoint controller
│   ├── config/                 # Application configuration schemas
│   │   ├── settings.py         # Pydantic BaseSettings class loading env variables
│   │   └── constants.py        # Domain & environmental configuration constants
│   ├── exceptions/             # Global exception handlers and error classes
│   │   └── handlers.py         # Standardized error mapping logic
│   ├── services/               # [Sprint 2+] Service layers (Empty placeholders)
│   ├── repositories/           # [Sprint 2+] Data access layers (Empty placeholders)
│   ├── schemas/                # [Sprint 2+] Pydantic request/response validation (Empty placeholders)
│   ├── simulation/             # [Sprint 2+] Physics simulation engines (Empty placeholders)
│   ├── ml/                     # [Sprint 2+] Machine learning models runner (Empty placeholders)
│   ├── utils/                  # Reusable utility modules
│   │   └── logger.py           # Configured Loguru structured logger
│   └── main.py                 # FastAPI Application entry point & lifespan
├── tests/                      # Core test suites
│   └── test_api.py             # Health endpoint and routing tests
├── Dockerfile                  # Container build instructions
├── requirements.txt            # Python dependencies manifest
└── README.md                   # Onboarding & architectural guide (This file)
```

---

## 🚀 Roadmap: Preparing for Sprint 2 (API Contract Design)

No business logic or backend functionality will be implemented in the next phase. Sprint 2 focuses purely on **API Contract Design**, including:
1. **API Versioning**: Implementing standardized version prefixes across routes.
2. **REST Endpoint Design**: Defining RESTful path structures for climate grids, forecasts, and hazard simulations.
3. **Request & Response Schemas**: Designing rigorous Pydantic schemas under `app/schemas/` to define input/output data constraints.
4. **Error Models**: Designing JSON error response models for validation, file parsing, and simulation failures.
5. **OpenAPI Documentation**: Automatically generating rich interactive Swagger documentation based on the schemas and paths.

---

## Local Setup and Installation

### Prerequisites
* Python 3.12+

### Installation Steps
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Set up and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Start the FastAPI development server:
```bash
.venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*(On macOS/Linux, replace `.venv\Scripts\uvicorn` with `.venv/bin/uvicorn`)*

### Interactive Swagger API Docs
* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Verification & Testing

Verify that the health check and root endpoints function correctly by running the automated pytest suite:
```bash
.venv\Scripts\python -m pytest tests/
```

### Health Check Endpoint Status
Querying `GET /health` or `GET /api/v1/health` returns:
```json
{
  "status": "healthy",
  "service": "PRITHVI Backend",
  "version": "0.1.0"
}
```
