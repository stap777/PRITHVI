"""
ML Model Predictor.

This module provides the high-level Predictor orchestrator that combines
ModelLoader (to load weight files) and InferenceEngine (to run maths transformations)
to produce final predictions for the Service Layer.

Classes:
    Predictor: High-level ML coordinator class.

TODO:
    * Connect model target classification to dynamically select weights.
"""

from typing import List
from loguru import logger

from app.ml.model_loader import ModelLoader
from app.ml.inference import InferenceEngine


class Predictor:
    """
    Orchestrates the loading, preprocessing, inference, and postprocessing of ML models.
    """

    def __init__(self):
        self.loader = ModelLoader()
        self.engine = InferenceEngine()

    def run_inference(
        self,
        lat: float,
        lon: float,
        metric: str,
        steps: int
    ) -> List[float]:
        """
        Runs ML prediction pipeline.
        
        Args:
            lat: Target latitude.
            lon: Target longitude.
            metric: Target variable (precipitation, temperature).
            steps: Future forecast length (months).
            
        Returns:
            List of floats representing predictions.
        """
        logger.info(f"Running ML inference pipeline for '{metric}' over {steps} steps.")

        # Determine appropriate model checkpoint name
        model_name = "convlstm_ensemble" if metric == "precipitation" else "xgboost_regressor"

        # 1. Load the model
        model = self.loader.get_model(model_name)

        # 2. Preprocess input parameters to tensor
        input_data = self.engine.preprocess_input(lat=lat, lon=lon, steps=steps)

        # 3. Execute model forward pass
        raw_outputs = self.engine.execute_forward_pass(model=model, input_tensor=input_data)

        # 4. Postprocess outputs to physical values
        final_forecast = self.engine.postprocess_output(raw_outputs)

        return final_forecast
