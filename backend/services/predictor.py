import os
import time
import torch
import numpy as np

# Import FraudDNN architecture
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.model import FraudDNN

class FraudPredictor:
    def __init__(self, model_path="models/best_focal_dnn.pt"):
        self.device = torch.device("cpu")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"PyTorch model not found at {model_path}")

        checkpoint = torch.load(model_path, map_location=self.device)
        self.feature_names = checkpoint.get("feature_names", [f"V{i}" for i in range(1, 29)] + ["Amount"])
        
        self.model = FraudDNN(in_features=len(self.feature_names)).to(self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    @staticmethod
    def _classify(probability: float, latency_ms: float = 0.0) -> dict:
        if probability >= 0.70:
            status, risk_tier, theme, headline = "BLOCKED", "High Risk", "danger", "Transaction Blocked"
        elif probability >= 0.30:
            status, risk_tier, theme, headline = "CHALLENGE", "Suspicious", "warning", "Verification Required"
        else:
            status, risk_tier, theme, headline = "APPROVED", "Safe", "success", "Transaction Approved"

        return {
            "fraud_probability": round(probability, 4),
            "risk_score_percent": round(probability * 100, 1),
            "status": status,
            "risk_tier": risk_tier,
            "theme": theme,
            "headline": headline,
            "latency_ms": round(latency_ms, 2)
        }

    def predict(self, scaled_features: np.ndarray) -> dict:
        """
        Runs inference on scaled feature array [1, 29] or [29,].
        Returns fraud probability, response latency, and decision status.
        """
        if scaled_features.ndim == 1:
            scaled_features = scaled_features.reshape(1, -1)
        tensor_input = torch.tensor(scaled_features, dtype=torch.float32).to(self.device)
        
        t0 = time.perf_counter()
        with torch.no_grad():
            logits = self.model(tensor_input)
            probability = float(torch.sigmoid(logits).cpu().numpy()[0, 0])
        latency_ms = (time.perf_counter() - t0) * 1000

        return self._classify(probability, latency_ms)

    def predict_batch(self, scaled_features_batch: np.ndarray) -> list:
        """
        Runs batched inference on [N, 29] array in a single forward pass.
        """
        if scaled_features_batch.ndim == 1:
            scaled_features_batch = scaled_features_batch.reshape(1, -1)
        tensor_input = torch.tensor(scaled_features_batch, dtype=torch.float32).to(self.device)
        
        with torch.no_grad():
            logits = self.model(tensor_input)
            probs = torch.sigmoid(logits).cpu().numpy().flatten()

        return [self._classify(float(p)) for p in probs]

