# Project PRITHVI – Climate Digital Twin using Machine Learning

## Overview

Project PRITHVI is an AI-powered Climate Digital Twin designed to predict climate variables using Machine Learning. The project uses Indian Meteorological Department (IMD) datasets and ERA5 climate datasets to build prediction models for:

* Rainfall
* Temperature
* Humidity

The backend is developed using **FastAPI**, while the machine learning models are trained using **XGBoost**.

---

# Technology Stack

### Programming Language

* Python 3.13

### Machine Learning

* XGBoost
* Scikit-Learn
* NumPy
* Pandas

### Climate Data Processing

* IMDLIB
* Xarray
* NetCDF4

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Model Storage

* Joblib
* XGBoost Native JSON

---

# Project Structure

```
DigitalTwinClimate/

│
├── app.py
├── requirements.txt
│
├── models/
│     ├── xgboost_rainfall_model.json
│     ├── temperature_xgboost.pkl
│     └── humidity_xgboost.pkl
│
├── notebooks/
│     ├── Rainfall.ipynb
│     ├── Temperature.ipynb
│     └── Humidity.ipynb
│
├── data/
│
│   ├── raw/
│   │      ├── rainfall/
│   │      ├── temperature/
│   │      └── humidity/
│   │
│   └── processed/
│
└── README.md
```

---

# Step 1 — Install Python

Download Python

https://www.python.org/downloads/

During installation enable

```
Add Python to PATH
```

---

# Step 2 — Create Virtual Environment

Open VS Code Terminal

```
python -m venv .venv
```

Activate

Windows

```
.venv\Scripts\activate
```

---

# Step 3 — Install Packages

```
pip install pandas
pip install numpy
pip install matplotlib
pip install xarray
pip install netCDF4
pip install imdlib
pip install xgboost
pip install scikit-learn
pip install fastapi
pip install uvicorn
pip install joblib
pip install pydantic
```

Or

```
pip install pandas numpy matplotlib xarray netCDF4 imdlib xgboost scikit-learn fastapi uvicorn joblib pydantic
```

---

# Step 4 — Download Datasets

## Rainfall

Download IMD Daily Rainfall

Store inside

```
data/raw/rainfall
```

---

## Temperature

Download IMD Tmax and Tmin

Store inside

```
data/raw/temperature/tmax

data/raw/temperature/tmin
```

---

## Humidity

Download ERA5 dataset from Copernicus Climate Data Store

Store

```
data/raw/humidity/test.nc
```

---

# Step 5 — Rainfall Notebook

### Load Dataset

```
imd.open_data()
```

### Convert Dataset

```
get_xarray()
```

### Feature Engineering

Create

* latitude
* longitude
* year
* month
* day
* hour
* dayofyear

### Train/Test Split

```
train_test_split()
```

### Train

```
XGBRegressor()
```

### Evaluate

* MAE
* RMSE
* R²

### Save Model

```
xgboost_rainfall_model.json
```

---

# Step 6 — Temperature Notebook

Load

```
tmax
```

Convert to DataFrame

Perform Feature Engineering

Create

* latitude
* longitude
* year
* month
* day
* hour
* dayofyear

Train

```
XGBRegressor
```

Evaluate

Save

```
temperature_xgboost.pkl
```

---

# Step 7 — Humidity Notebook

Load

```
test.nc
```

Convert Dataset

```
xarray → DataFrame
```

Feature Engineering

Create

* latitude
* longitude
* year
* month
* day
* hour
* dayofyear

Train

```
XGBRegressor
```

Evaluate

Save

```
humidity_xgboost.pkl
```

---

# Step 8 — FastAPI

Create

```
app.py
```

Load Models

```
Rainfall

Temperature

Humidity
```

Create Endpoints

```
GET /

GET /health

POST /api/v1/predict/rainfall

POST /api/v1/predict/temperature

POST /api/v1/predict/humidity
```

---

# Step 9 — Run Backend

```
uvicorn app:app --reload
```

If file name is

```
aap.py
```

Run

```
uvicorn aap:app --reload
```

---

# Step 10 — Swagger

Open

```
http://127.0.0.1:8000/docs
```

Available APIs

```
GET /health

POST /api/v1/predict/rainfall

POST /api/v1/predict/temperature

POST /api/v1/predict/humidity
```

---

# Step 11 — Example Request

Temperature

```json
{
  "latitude": 19.076,
  "longitude": 72.877,
  "year": 2025,
  "month": 7,
  "day": 10,
  "hour": 0,
  "dayofyear": 191
}
```

---

Rainfall

```json
{
  "latitude": 19.076,
  "longitude": 72.877,
  "year": 2025,
  "month": 7,
  "day": 10,
  "hour": 0,
  "dayofyear": 191
}
```

---

Humidity

```json
{
  "latitude": 19.076,
  "longitude": 72.877,
  "year": 2025,
  "month": 7,
  "day": 10,
  "hour": 12,
  "dayofyear": 191
}
```

---

# Model Evaluation Metrics

The project evaluates all trained models using:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

---

# Output

After training, the models are stored in the `models/` directory and used by the FastAPI backend to provide real-time predictions through REST APIs.

---

# Future Enhancements

* 7-day Climate Forecasting
* Flood Risk Prediction
* Heatwave Detection
* Drought Prediction
* Land Surface Temperature (LST)
* Sea Surface Temperature (SST)
* Interactive Dashboard
* GIS Visualization
* Satellite Data Integration (INSAT)
* District-wise Climate Digital Twin
