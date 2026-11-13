import time
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    ConfusionMatrixDisplay
)
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Set seeds for reproducibility
np.random.seed(42)
torch.manual_seed(42)

print("=" * 80)
print("  MULTI-MODEL FINANCIAL FRAUD DETECTION BENCHMARKING ENGINE")
print("  Trained on the Exact Same Dataset (ULB European Credit Card Benchmark)")
print("=" * 80)

# -------------------------------------------------------------
# 1. DATA PREPARATION & LEAKAGE-FREE SPLIT
# -------------------------------------------------------------
print("\n[Step 1/5] Loading and Preprocessing Data...")
df = pd.read_csv("creditcard.csv")
original_len = len(df)
df = df.drop_duplicates()
dedup_len = len(df)
print(f"  • Raw transactions: {original_len:,}")
print(f"  • After deduplication (Albalawi & Dardouri 2025): {dedup_len:,} (-{original_len - dedup_len:,} duplicates)")
print(f"  • Fraud cases: {df['Class'].sum():,} ({df['Class'].mean()*100:.3f}%)")

X = df.drop(columns=['Class', 'Time'])
y = df['Class']

# 80/20 Stratified Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"  • Train set: {len(X_train):,} samples ({y_train.sum()} frauds)")
print(f"  • Test set:  {len(X_test):,} samples ({y_test.sum()} frauds)")

# Scaling fit STRICTLY on training split
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Resampling Training Split with SMOTE (k=5)
print("  • Applying SMOTE (k=5) to Training partition only...")
smote = SMOTE(k_neighbors=5, random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
print(f"  • Balanced Train set: {len(X_train_smote):,} samples (50% fraud / 50% legitimate)")

# -------------------------------------------------------------
# 2. MODEL DEFINITIONS
# -------------------------------------------------------------
results = []
trained_models = {}

models_dict = {
    "Logistic Regression": (
        LogisticRegression(C=0.1, solver='liblinear', random_state=42),
        X_train_smote, y_train_smote
    ),
    "Decision Tree": (
        DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=42),
        X_train_smote, y_train_smote
    ),
    "Random Forest": (
        RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42),
        X_train_smote, y_train_smote
    ),
    "XGBoost": (
        XGBClassifier(n_estimators=150, max_depth=5, learning_rate=0.1, eval_metric='logloss', random_state=42, n_jobs=-1),
        X_train_smote, y_train_smote
    ),
    "LightGBM": (
        LGBMClassifier(n_estimators=150, max_depth=5, learning_rate=0.1, random_state=42, n_jobs=-1, verbose=-1),
        X_train_smote, y_train_smote
    )
}

# -------------------------------------------------------------
# 3. TRAINING & EVALUATING SKLEARN / BOOSTING MODELS
# -------------------------------------------------------------
print("\n[Step 2/5] Training Classical & Ensemble Machine Learning Models...")

for name, (clf, x_tr, y_tr) in models_dict.items():
    print(f"  --> Training {name}...")
    t0 = time.time()
    clf.fit(x_tr, y_tr)
    train_time = time.time() - t0
    trained_models[name] = clf

    # Latency per single transaction
    t_start = time.perf_counter()
    y_pred = clf.predict(X_test_scaled)
    t_end = time.perf_counter()
    latency_ms = ((t_end - t_start) / len(X_test_scaled)) * 1000

    y_prob = clf.predict_proba(X_test_scaled)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, y_pred) * 100
    prec = precision_score(y_test, y_pred, zero_division=0) * 100
    rec = recall_score(y_test, y_pred) * 100
    f1 = f1_score(y_test, y_pred) * 100
    roc_auc = roc_auc_score(y_test, y_prob)
    auprc = average_precision_score(y_test, y_prob)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    # Economic Loss: CFN = $150, CFP = $3 (Yang et al., 2026)
    econ_loss = (fn * 150.0) + (fp * 3.0)

    results.append({
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
        "Latency (ms/txn)": round(latency_ms, 3)
    })
    print(f"      Acc: {acc:.2f}% | Prec: {prec:.2f}% | Rec: {rec:.2f}% | F1: {f1:.2f}% | FP: {fp} | FN: {fn}")

# -------------------------------------------------------------
# 4. TRAINING DEEP LEARNING MODEL WITH FOCAL LOSS
# -------------------------------------------------------------
print("\n[Step 3/5] Training Deep Neural Network with Binary Focal Loss (Native Imbalanced Data)...")

class BinaryFocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0):
        super(BinaryFocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, logits, targets):
        bce = nn.functional.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        pt = torch.exp(-bce)
        focal_loss = self.alpha * ((1 - pt) ** self.gamma) * bce
        return focal_loss.mean()

class FraudDNN(nn.Module):
    def __init__(self, in_features):
        super(FraudDNN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 256),
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
print(f"  • Using Device: {device}")

# Prepare PyTorch Tensors on NATIVE imbalanced training data
train_dataset = TensorDataset(
    torch.tensor(X_train_scaled, dtype=torch.float32),
    torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)
)
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)

test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)

model_dl = FraudDNN(X_train_scaled.shape[1]).to(device)
criterion = BinaryFocalLoss(alpha=0.25, gamma=2.0)
optimizer = optim.Adam(model_dl.parameters(), lr=0.001)

# Training loop
epochs = 12
model_dl.train()
for ep in range(epochs):
    ep_loss = 0.0
    for bx, by in train_loader:
        bx, by = bx.to(device), by.to(device)
        optimizer.zero_grad()
        out = model_dl(bx)
        loss = criterion(out, by)
        loss.backward()
        optimizer.step()
        ep_loss += loss.item()
    if (ep + 1) % 4 == 0 or ep == epochs - 1:
        print(f"      Epoch [{ep+1}/{epochs}] - Loss: {ep_loss/len(train_loader):.5f}")

# Inference on Test Set
model_dl.eval()
with torch.no_grad():
    t_start = time.perf_counter()
    logits = model_dl(test_tensor)
    t_end = time.perf_counter()
    dl_latency = ((t_end - t_start) / len(X_test_scaled)) * 1000
    
    probs = torch.sigmoid(logits).cpu().numpy().flatten()
    dl_preds = (probs >= 0.5).astype(int)

dl_acc = accuracy_score(y_test, dl_preds) * 100
dl_prec = precision_score(y_test, dl_preds, zero_division=0) * 100
dl_rec = recall_score(y_test, dl_preds) * 100
dl_f1 = f1_score(y_test, dl_preds) * 100
dl_roc_auc = roc_auc_score(y_test, probs)
dl_auprc = average_precision_score(y_test, probs)
tn, fp, fn, tp = confusion_matrix(y_test, dl_preds).ravel()
dl_econ_loss = (fn * 150.0) + (fp * 3.0)

results.append({
    "Model": "Deep Learning (Focal Loss)",
    "Accuracy (%)": round(dl_acc, 4),
    "Precision (%)": round(dl_prec, 2),
    "Recall (%)": round(dl_rec, 2),
    "F1-Score (%)": round(dl_f1, 2),
    "ROC-AUC": round(dl_roc_auc, 4),
    "AUPRC": round(dl_auprc, 4),
    "False Positives": fp,
    "False Negatives": fn,
    "Operational Cost ($)": round(dl_econ_loss, 2),
    "Latency (ms/txn)": round(dl_latency, 3)
})
print(f"      Acc: {dl_acc:.2f}% | Prec: {dl_prec:.2f}% | Rec: {dl_rec:.2f}% | F1: {dl_f1:.2f}% | FP: {fp} | FN: {fn}")

# -------------------------------------------------------------
# 5. GENERATE FINAL REPORT & COMPARISON VISUALS
# -------------------------------------------------------------
print("\n[Step 4/5] Generating Summary Table and Visualizations...")
res_df = pd.DataFrame(results)
res_df.to_csv("model_comparison_results.csv", index=False)

print("\n" + "=" * 95)
print(res_df.to_string(index=False))
print("=" * 95)

# Visual Comparison Chart
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Accuracy vs F1-Score
x = np.arange(len(res_df))
width = 0.35

axes[0].bar(x - width/2, res_df["Accuracy (%)"], width, label="Accuracy (%)", color="#3b82f6")
axes[0].bar(x + width/2, res_df["F1-Score (%)"], width, label="F1-Score (%)", color="#ef4444")
axes[0].set_ylabel("Score (%)")
axes[0].set_title("Accuracy vs F1-Score: The Accuracy Paradox Illustrated")
axes[0].set_xticks(x)
axes[0].set_xticklabels(res_df["Model"], rotation=25, ha="right")
axes[0].set_ylim(0, 105)
axes[0].legend()
axes[0].grid(axis="y", linestyle="--", alpha=0.5)

# Plot 2: Precision vs Recall Trade-Off
axes[1].bar(x - width/2, res_df["Precision (%)"], width, label="Precision (%) [Low False Positives]", color="#10b981")
axes[1].bar(x + width/2, res_df["Recall (%)"], width, label="Recall (%) [Low Missed Fraud]", color="#f59e0b")
axes[1].set_ylabel("Score (%)")
axes[1].set_title("Precision vs Recall Performance Across All Models")
axes[1].set_xticks(x)
axes[1].set_xticklabels(res_df["Model"], rotation=25, ha="right")
axes[1].set_ylim(0, 105)
axes[1].legend()
axes[1].grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("models_benchmark_chart.png", dpi=300)
plt.close()
print("  • Saved comparative performance chart to 'models_benchmark_chart.png'")

print("\n[Step 5/5] Benchmarking complete! Results saved to 'model_comparison_results.csv'.")
