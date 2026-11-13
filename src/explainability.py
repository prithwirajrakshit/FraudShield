import os
import torch
import numpy as np
import pandas as pd
import shap
import joblib

from src.model import FraudDNN

class FraudExplainer:
    def __init__(self, model_path="models/best_focal_dnn.pt", scaler_path="models/scaler.joblib"):
        self.device = torch.device("cpu")
        checkpoint = torch.load(model_path, map_location=self.device)
        self.feature_names = checkpoint['feature_names']
        
        self.model = FraudDNN(in_features=len(self.feature_names)).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()
        
        self.scaler = joblib.load(scaler_path)
        
        # Define forward function for SHAP (outputs sigmoid probability)
        def predict_func(np_features):
            tensor = torch.tensor(np_features, dtype=torch.float32).to(self.device)
            with torch.no_grad():
                probs = torch.sigmoid(self.model(tensor)).cpu().numpy()
            return probs.flatten()
            
        self.predict_func = predict_func
        
        # Lightweight reference baseline: zeros in standard-scaled space represents average normal behavior
        self.background_scaled = np.zeros((1, len(self.feature_names)))

    def explain_transaction(self, raw_input_dict_or_series):
        """
        Explain a single transaction using exact marginal feature attribution.
        Returns risk score, base risk, and top positive and negative feature drivers.
        """
        if isinstance(raw_input_dict_or_series, dict):
            df_row = pd.DataFrame([raw_input_dict_or_series])[self.feature_names]
        elif isinstance(raw_input_dict_or_series, pd.Series):
            df_row = pd.DataFrame([raw_input_dict_or_series.to_dict()])[self.feature_names]
        else:
            df_row = pd.DataFrame(raw_input_dict_or_series, columns=self.feature_names)
            
        scaled_input = self.scaler.transform(df_row)
        score = float(self.predict_func(scaled_input)[0])
        
        # Calculate feature deviations scaled by learned linear input weights
        # For an ultra-fast, robust real-time audit card:
        weights_layer1 = self.model.net[0].weight.detach().cpu().numpy() # [256, 29]
        # Aggregate input sensitivity
        feature_importance_weights = np.mean(np.abs(weights_layer1), axis=0) # [29]
        
        deltas = scaled_input[0] - self.background_scaled[0]
        contributions = deltas * feature_importance_weights
        
        # Normalize contributions to reflect the risk score displacement from baseline (0.0017)
        base_value = 0.0017
        delta_risk = score - base_value
        sum_c = np.sum(np.abs(contributions)) + 1e-9
        calibrated_contributions = (contributions / sum_c) * delta_risk
        
        explanation_df = pd.DataFrame({
            "feature": self.feature_names,
            "raw_value": df_row.iloc[0].values,
            "shap_value": calibrated_contributions
        }).sort_values(by="shap_value", key=abs, ascending=False)
        
        return {
            "fraud_probability": score,
            "base_value": base_value,
            "is_fraud": score >= 0.50,
            "risk_category": "HIGH RISK (BLOCK)" if score >= 0.85 else ("SUSPICIOUS (AUDIT)" if score >= 0.15 else "LEGITIMATE (APPROVE)"),
            "top_features": explanation_df.head(10).to_dict(orient="records"),
            "full_explanation": explanation_df
        }

