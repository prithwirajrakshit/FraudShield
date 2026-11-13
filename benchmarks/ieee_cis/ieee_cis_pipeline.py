import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Reproducibility
np.random.seed(42)
torch.manual_seed(42)

print("=" * 80)
print("  IEEE-CIS FRAUD DETECTION BENCHMARKING ENGINE")
print("  Evaluating All 6 Models on the Exact Same Dataset Partition")
print("=" * 80)

def reduce_mem_usage(df):
    """Downcast numeric types to reduce memory footprint."""
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtype
        if col_type != object and not isinstance(col_type, pd.CategoricalDtype):
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
            else:
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
    end_mem = df.memory_usage().sum() / 1024**2
    print(f"  • Memory reduced: {start_mem:.2f} MB --> {end_mem:.2f} MB ({(start_mem - end_mem)/start_mem * 100:.1f}% savings)")
    return df

def run_pipeline():
    tx_file = "train_transaction.csv"
    if not os.path.exists(tx_file):
        print(f"[ERROR] {tx_file} not found.")
        return

    # 1. LOAD DATA
    print("\n[Step 1/5] Loading IEEE-CIS Transaction Data...")
    t0 = time.time()
    df = pd.read_csv(tx_file)
    print(f"  • Successfully loaded {len(df):,} transactions in {time.time()-t0:.2f} seconds.")
    print(f"  • Total Columns: {df.shape[1]}")
    print(f"  • Total Fraud Events: {df['isFraud'].sum():,} ({df['isFraud'].mean()*100:.2f}%)")

    # 2. FEATURE ENGINEERING & MISSING VALUE PRUNING
    print("\n[Step 2/5] Cleaning & Preprocessing Features...")
    df = reduce_mem_usage(df)

    # Prune columns with > 60% missing data
    null_threshold = 0.60
    missing_rates = df.isnull().mean()
    high_null_cols = missing_rates[missing_rates > null_threshold].index.tolist()
    df = df.drop(columns=high_null_cols)
    print(f"  • Removed {len(high_null_cols)} columns with >{null_threshold*100}% missing values.")

    target_col = 'isFraud'
    drop_cols = ['TransactionID', 'TransactionDT', target_col]
    feature_cols = [c for c in df.columns if c not in drop_cols]

    # Frequency encode categorical variables
    cat_cols = df[feature_cols].select_dtypes(include=['object']).columns
    print(f"  • Frequency-encoding {len(cat_cols)} categorical attributes...")
    for col in cat_cols:
        freq = df[col].value_counts(normalize=True).to_dict()
        df[col] = df[col].map(freq).fillna(0)

    # Impute remaining numerical nulls with median
    num_cols = df[feature_cols].select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    X = df[feature_cols]
    y = df[target_col].astype(int)

    # Stratified sample of 120,000 records for fast, balanced academic execution
    if len(df) > 120000:
        print(f"  • Stratified sampling 120,000 instances from {len(df):,} (preserves exact 3.5% fraud ratio)...")
        X, _, y, _ = train_test_split(X, y, train_size=120000, random_state=42, stratify=y)

    # 3. LEAKAGE-FREE SPLIT & SCALING
    print("\n[Step 3/5] Stratified 80/20 Train-Test Splitting & Scaling...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"  • Training Partition: {len(X_train):,} samples ({y_train.sum():,} fraud cases)")
    print(f"  • Testing Partition:  {len(X_test):,} samples ({y_test.sum():,} fraud cases)")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. MODEL BENCHMARKING
    print("\n[Step 4/5] Training All Models on the Exact Same Split...")
    models = {
        "Logistic Regression": LogisticRegression(C=0.1, max_iter=500, solver='liblinear', random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, min_samples_split=10, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.1, eval_metric='logloss', random_state=42, n_jobs=-1),
        "LightGBM": LGBMClassifier(n_estimators=150, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1, verbose=-1)
    }

    results = []

    for name, clf in models.items():
        print(f"  --> Training {name}...")
        t_fit = time.perf_counter()
        clf.fit(X_train_scaled, y_train)
        fit_time = time.perf_counter() - t_fit

        t_inf = time.perf_counter()
        y_pred = clf.predict(X_test_scaled)
        inf_time = time.perf_counter() - t_inf
        lat_ms = (inf_time / len(X_test_scaled)) * 1000

        y_prob = clf.predict_proba(X_test_scaled)[:, 1]

        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred, zero_division=0) * 100
        rec = recall_score(y_test, y_pred) * 100
        f1 = f1_score(y_test, y_pred) * 100
        roc_auc = roc_auc_score(y_test, y_prob)
        auprc = average_precision_score(y_test, y_prob)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        econ_loss = (fn * 150.0) + (fp * 3.0)

        results.append({
            "Dataset": "IEEE-CIS Fraud",
            "Model": name,
            "Accuracy (%)": round(acc, 4),
            "Precision (%)": round(prec, 2),
            "Recall (%)": round(rec, 2),
            "F1-Score (%)": round(f1, 2),
            "ROC-AUC": round(roc_auc, 4),
            "AUPRC": round(auprc, 4),
            "False Positives": fp,
            "False Negatives": fn,
            "Operational Cost ($)": round(econ_loss, 2),
            "Latency (ms/txn)": round(lat_ms, 3)
        })
        print(f"      Acc: {acc:.2f}% | Prec: {prec:.2f}% | Rec: {rec:.2f}% | F1: {f1:.2f}% | FP: {fp} | FN: {fn}")

    # Deep Neural Network with Focal Loss
    print("  --> Training Deep Neural Network (with Binary Focal Loss)...")
    class BinaryFocalLoss(nn.Module):
        def __init__(self, alpha=0.25, gamma=2.0):
            super().__init__()
            self.alpha = alpha
            self.gamma = gamma
        def forward(self, logits, targets):
            bce = nn.functional.binary_cross_entropy_with_logits(logits, targets, reduction='none')
            pt = torch.exp(-bce)
            return (self.alpha * ((1 - pt) ** self.gamma) * bce).mean()

    class IEEENet(nn.Module):
        def __init__(self, in_dim):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_dim, 256),
                nn.BatchNorm1d(256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 64),
                nn.BatchNorm1d(64),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(64, 1)
            )
        def forward(self, x):
            return self.net(x)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_ds = TensorDataset(torch.tensor(X_train_scaled, dtype=torch.float32), torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1))
    train_ld = DataLoader(train_ds, batch_size=256, shuffle=True)
    test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)

    dl_model = IEEENet(X_train_scaled.shape[1]).to(device)
    criterion = BinaryFocalLoss(alpha=0.25, gamma=2.0)
    optimizer = optim.Adam(dl_model.parameters(), lr=0.001)

    dl_model.train()
    for ep in range(12):
        for bx, by in train_ld:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = dl_model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()

    dl_model.eval()
    with torch.no_grad():
        t0 = time.perf_counter()
        logits = dl_model(test_tensor)
        dl_lat = ((time.perf_counter() - t0) / len(X_test_scaled)) * 1000
        probs = torch.sigmoid(logits).cpu().numpy().flatten()
        preds = (probs >= 0.5).astype(int)

    acc = accuracy_score(y_test, preds) * 100
    prec = precision_score(y_test, preds, zero_division=0) * 100
    rec = recall_score(y_test, preds) * 100
    f1 = f1_score(y_test, preds) * 100
    roc_auc = roc_auc_score(y_test, probs)
    auprc = average_precision_score(y_test, probs)
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
    econ_loss = (fn * 150.0) + (fp * 3.0)

    results.append({
        "Dataset": "IEEE-CIS Fraud",
        "Model": "Deep Learning (Focal Loss)",
        "Accuracy (%)": round(acc, 4),
        "Precision (%)": round(prec, 2),
        "Recall (%)": round(rec, 2),
        "F1-Score (%)": round(f1, 2),
        "ROC-AUC": round(roc_auc, 4),
        "AUPRC": round(auprc, 4),
        "False Positives": fp,
        "False Negatives": fn,
        "Operational Cost ($)": round(econ_loss, 2),
        "Latency (ms/txn)": round(dl_lat, 3)
    })
    print(f"      Acc: {acc:.2f}% | Prec: {prec:.2f}% | Rec: {rec:.2f}% | F1: {f1:.2f}% | FP: {fp} | FN: {fn}")

    # 5. SUMMARY AND PLOTTING
    print("\n[Step 5/5] Generating Output Table and Benchmark Chart...")
    res_df = pd.DataFrame(results)
    res_df.to_csv("ieee_cis_model_comparison.csv", index=False)

    print("\n" + "=" * 95)
    print(res_df.to_string(index=False))
    print("=" * 95)

    # Plotting comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    x = np.arange(len(res_df))
    width = 0.35

    axes[0].bar(x - width/2, res_df["Accuracy (%)"], width, label="Accuracy (%)", color="#2563eb")
    axes[0].bar(x + width/2, res_df["F1-Score (%)"], width, label="F1-Score (%)", color="#dc2626")
    axes[0].set_ylabel("Score (%)")
    axes[0].set_title("IEEE-CIS Fraud: Accuracy vs F1-Score")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(res_df["Model"], rotation=25, ha="right")
    axes[0].set_ylim(0, 105)
    axes[0].legend()
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)

    axes[1].bar(x - width/2, res_df["Precision (%)"], width, label="Precision (%)", color="#059669")
    axes[1].bar(x + width/2, res_df["Recall (%)"], width, label="Recall (%)", color="#d97706")
    axes[1].set_ylabel("Score (%)")
    axes[1].set_title("IEEE-CIS Fraud: Precision vs Recall Trade-Off")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(res_df["Model"], rotation=25, ha="right")
    axes[1].set_ylim(0, 105)
    axes[1].legend()
    axes[1].grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("ieee_cis_benchmark_chart.png", dpi=300)
    plt.close()
    print("  • Saved comparison chart to 'ieee_cis_benchmark_chart.png'")
    print("  • Saved CSV table to 'ieee_cis_model_comparison.csv'")
    print("\nBenchmarking complete!")

if __name__ == "__main__":
    run_pipeline()
