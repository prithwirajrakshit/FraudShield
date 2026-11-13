import os
import json
import time
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)

from src.data_pipeline import load_and_preprocess_data
from src.model import FraudDNN
from src.focal_loss import BinaryFocalLoss

def train_focal_dnn(epochs=12, batch_size=128, lr=0.001, alpha=0.25, gamma=2.0):
    np.random.seed(42)
    torch.manual_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[Training] Hardware execution device: {device}")
    
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Load data
    data = load_and_preprocess_data()
    X_train_scaled = data["X_train_scaled"]
    X_test_scaled = data["X_test_scaled"]
    y_train = data["y_train"]
    y_test = data["y_test"]
    scaler = data["scaler"]
    feature_names = data["feature_names"]
    
    # Save fitted scaler
    joblib.dump(scaler, os.path.join("models", "scaler.joblib"))
    print("[Training] Fitted StandardScaler saved to models/scaler.joblib")
    
    # Save a set of test samples for instant Streamlit UI testing
    X_test_df = data["X_test_raw"].copy()
    X_test_df["Actual_Class"] = y_test.values
    sample_legit = X_test_df[X_test_df["Actual_Class"] == 0].head(15)
    sample_fraud = X_test_df[X_test_df["Actual_Class"] == 1].head(15)
    samples = pd.concat([sample_legit, sample_fraud]).reset_index(drop=True)
    samples.to_csv(os.path.join("data", "sample_transactions.csv"), index=False)
    print("[Training] Saved curated test samples to data/sample_transactions.csv")
    
    # Setup PyTorch Tensors on NATIVE imbalanced training data
    train_dataset = TensorDataset(
        torch.tensor(X_train_scaled, dtype=torch.float32),
        torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)
    )
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)
    
    model = FraudDNN(in_features=X_train_scaled.shape[1]).to(device)
    criterion = BinaryFocalLoss(alpha=alpha, gamma=gamma)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    print(f"\n[Training] Commencing Deep Neural Network training ({epochs} epochs)...")
    t0 = time.time()
    model.train()
    for ep in range(epochs):
        ep_loss = 0.0
        for bx, by in train_loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            ep_loss += loss.item()
        avg_loss = ep_loss / len(train_loader)
        if (ep + 1) % 3 == 0 or ep == epochs - 1:
            print(f"  • Epoch [{ep+1:02d}/{epochs:02d}] - Focal Loss: {avg_loss:.6f}")
            
    train_time = time.time() - t0
    print(f"[Training] Model training completed in {train_time:.2f} seconds.")
    
    # Evaluation on held-out test split
    print("\n[Evaluation] Evaluating on 56,746 held-out test transactions...")
    model.eval()
    with torch.no_grad():
        t_start = time.perf_counter()
        logits = model(test_tensor)
        t_end = time.perf_counter()
        lat_per_txn_ms = ((t_end - t_start) / len(X_test_scaled)) * 1000
        
        probs = torch.sigmoid(logits).cpu().numpy().flatten()
        preds = (probs >= 0.5).astype(int)
        
    acc = accuracy_score(y_test, preds) * 100
    prec = precision_score(y_test, preds, zero_division=0) * 100
    rec = recall_score(y_test, preds) * 100
    f1 = f1_score(y_test, preds) * 100
    roc_auc = roc_auc_score(y_test, probs)
    auprc = average_precision_score(y_test, probs)
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
    operational_cost = (fn * 150.0) + (fp * 3.0)
    
    metrics = {
        "model_name": "Deep Learning (Binary Focal Loss)",
        "accuracy_pct": round(acc, 4),
        "precision_pct": round(prec, 2),
        "recall_pct": round(rec, 2),
        "f1_score_pct": round(f1, 2),
        "roc_auc": round(roc_auc, 4),
        "auprc": round(auprc, 4),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "operational_cost_dollars": round(operational_cost, 2),
        "latency_ms_per_txn": round(lat_per_txn_ms, 3),
        "total_test_samples": len(y_test),
        "total_test_frauds": int(y_test.sum())
    }
    
    print("\n" + "=" * 65)
    print("  EMPIRICAL EVALUATION RESULTS - DEEP FOCAL NETWORK")
    print("=" * 65)
    print(f"  • Accuracy:           {acc:.4f}%")
    print(f"  • Precision:          {prec:.2f}% (Only {fp} false alarms out of {len(y_test):,} txns!)")
    print(f"  • Recall:             {rec:.2f}% ({tp} out of {y_test.sum()} frauds caught)")
    print(f"  • F1-Score:           {f1:.2f}%")
    print(f"  • ROC-AUC:            {roc_auc:.4f}")
    print(f"  • AUPRC:              {auprc:.4f}")
    print(f"  • Operational Loss:   ${operational_cost:,.2f}")
    print(f"  • Inference Latency:  {lat_per_txn_ms:.3f} ms / transaction (CPU)")
    print("=" * 65)
    
    # Save checkpoint
    torch.save({
        'model_state_dict': model.state_dict(),
        'feature_names': feature_names,
        'hyperparameters': {
            'in_features': len(feature_names),
            'alpha': alpha,
            'gamma': gamma,
            'epochs': epochs
        }
    }, os.path.join("models", "best_focal_dnn.pt"))
    print("[Training] Model weights saved to models/best_focal_dnn.pt")
    
    # Save metrics JSON
    with open(os.path.join("models", "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
    print("[Training] Evaluation metrics saved to models/metrics.json")
    
    return metrics

if __name__ == "__main__":
    train_focal_dnn()

