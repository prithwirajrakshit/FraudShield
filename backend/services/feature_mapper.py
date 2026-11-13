import numpy as np
import pandas as pd
import joblib
import os

class FeatureMapper:
    """
    Translates consumer-friendly transaction inputs into the model's 29-dimensional
    behavioral feature space (V1-V28, Amount) and normalizes them using the fitted StandardScaler.
    """
    def __init__(self, scaler_path="models/scaler.joblib"):
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")
        self.scaler = joblib.load(scaler_path)
        self.feature_names = [f"V{i}" for i in range(1, 29)] + ["Amount"]

        # Category baseline risk multipliers
        self.category_weights = {
            "grocery": 0.05,
            "dining": 0.08,
            "utilities": 0.04,
            "transport": 0.06,
            "clothing": 0.15,
            "electronics": 0.45,
            "travel": 0.50,
            "jewelry": 0.65,
            "gaming": 0.60,
            "crypto": 0.85,
            "wire_transfer": 0.80,
            "general": 0.10
        }

        # Channel risk multipliers
        self.channel_weights = {
            "in_store_chip": 0.02,
            "contactless": 0.05,
            "online": 0.35,
            "atm": 0.20,
            "card_not_present": 0.55
        }

    def map_to_features(
        self,
        amount: float,
        merchant_category: str = "general",
        channel: str = "online",
        is_foreign: bool = False,
        is_night_time: bool = False,
        device_trusted: bool = True,
        user_avg_amount: float = 50.0,
        velocity_1h: int = 1
    ) -> np.ndarray:
        """
        Synthesizes calibrated latent behavioral coordinates from human transaction parameters.
        """
        # 1. Amount Anomaly Ratio
        avg_amt = max(user_avg_amount, 5.0)
        amount_ratio = amount / avg_amt
        
        # 2. Risk Factors
        cat_risk = self.category_weights.get(merchant_category.lower(), 0.10)
        chan_risk = self.channel_weights.get(channel.lower(), 0.20)
        foreign_penalty = 1.8 if is_foreign else 0.0
        night_penalty = 1.2 if is_night_time else 0.0
        device_penalty = 1.5 if not device_trusted else 0.0
        velocity_penalty = max(0.0, (velocity_1h - 1) * 0.7)

        # Composite behavioral deviation score
        total_anomaly = (
            (amount_ratio - 1.0) * 0.4
            + cat_risk * 2.0
            + chan_risk * 1.5
            + foreign_penalty
            + night_penalty
            + device_penalty
            + velocity_penalty
        )

        # Map to latent components (calibrated against empirical PCA fraud clusters)
        # In ULB dataset:
        # Fraud cases strongly shift: V14 negative, V10 negative, V12 negative, V4 positive, V11 positive
        v_vector = np.zeros(28)
        
        # Base normal transaction noise
        np.random.seed(int(amount * 100) % 10000)
        v_vector += np.random.normal(0, 0.2, 28)

        if total_anomaly > 1.0:
            # Shift primary fraud discriminative axes proportionally
            factor = min(total_anomaly, 8.0)
            v_vector[13] = -1.2 * factor     # V14 (Index 13)
            v_vector[9]  = -0.9 * factor     # V10 (Index 9)
            v_vector[11] = -0.8 * factor     # V12 (Index 11)
            v_vector[3]  = 0.7 * factor      # V4 (Index 3)
            v_vector[10] = 0.6 * factor      # V11 (Index 10)
            v_vector[16] = -0.5 * factor     # V17 (Index 16)
        else:
            # Legitimate purchase profile
            v_vector[13] = 0.1
            v_vector[9]  = 0.05
            v_vector[11] = 0.1

        # Full feature vector with raw Amount wrapped in DataFrame to preserve feature names
        feature_df = pd.DataFrame(
            np.append(v_vector, amount).reshape(1, -1),
            columns=self.feature_names
        )
        
        # Standardize using the model's fitted scaler
        scaled_features = self.scaler.transform(feature_df)
        return scaled_features
