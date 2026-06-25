"""
AI Prediction Business Service.

This service acts as the orchestrator for loading machine learning models
and running inference. It bridges the REST endpoints with the core ML layer.

Classes:
    PredictionService: Business logic handlers for AI weather forecasts.

TODO:
    * Integrate actual Predictor class execution.
    * Add support for spatial tensor output mapping.
"""

from typing import Dict, Any
from loguru import logger

from app.schemas.prediction import PredictionRequest, PredictionResponse, ForecastObservation
from app.ml.predictor import Predictor # will be imported and used


class PredictionService:
    """
    Orchestrates ML pipeline execution, loading checkpoints, and preparing predictions.
    """

    def __init__(self):
        # Initialize ML Predictor coordinator
        self.predictor = Predictor()

    def predict_metric(self, request: PredictionRequest) -> PredictionResponse:
        """
        Executes model forecast predictions for coordinates and metric.
        
        Args:
            request: Latitude/longitude target and prediction horizon.
            
        Returns:
            PredictionResponse containing simulated future weather.
        """
        logger.info(
            f"Triggering ML forecast on metric '{request.target_metric}' using "
            f"model '{request.model_name}' for {request.horizon_months} months."
        )
        
        # Invoke low-level model predictor (returns mock values for now)
        raw_forecast = self.predictor.run_inference(
            lat=request.latitude,
            lon=request.longitude,
            metric=request.target_metric,
            steps=request.horizon_months
        )
        
        # Format ML raw floats into API response structure
        predictions = []
        for i, val in enumerate(raw_forecast):
            # Calculate mock monthly increments
            month_idx = (i % 12) + 1
            year_offset = i // 12
            year = 2026 + year_offset
            date_str = f"{year}-{month_idx:02d}"
            
            obs = ForecastObservation(
                timestep_index=i,
                date_label=date_str,
                predicted_value=val,
                confidence_lower=val * 0.9,
                confidence_upper=val * 1.1
            )
            predictions.append(obs)

        return PredictionResponse(
            latitude=request.latitude,
            longitude=request.longitude,
            target_metric=request.target_metric,
            horizon_months=request.horizon_months,
            model_version="ConvLSTM_v1.4.2_checkpoints_2026",
            predictions=predictions
        )

    def get_available_models(self) -> Dict[str, Any]:
        """
        Inspects model inventory.
        
        Returns:
            Dict containing details of available model versions.
        """
        logger.info("Retrieving list of configured machine learning model architectures.")
        return {
            "default_model": "convlstm_ensemble",
            "active_models": [
                {
                    "name": "convlstm_ensemble",
                    "target_metric": "precipitation",
                    "resolution": "0.1 deg",
                    "last_updated": "2026-05-10"
                },
                {
                    "name": "xgboost_regressor",
                    "target_metric": "surface_temperature",
                    "resolution": "0.25 deg",
                    "last_updated": "2026-04-18"
                }
            ]
        }
