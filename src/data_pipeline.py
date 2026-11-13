import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

def find_dataset_path():
    candidate_paths = [
        os.path.join("data", "creditcard.csv"),
        os.path.join("ULB_Credit_Card_Benchmark", "creditcard.csv"),
        "creditcard.csv",
        os.path.join("..", "ULB_Credit_Card_Benchmark", "creditcard.csv")
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("Could not locate creditcard.csv. Please place it in data/ or ULB_Credit_Card_Benchmark/.")

def load_and_preprocess_data(dataset_path=None, test_size=0.20, random_state=42):
    if dataset_path is None:
        dataset_path = find_dataset_path()
        
    print(f"[Data Pipeline] Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    initial_count = len(df)
    
    # Step 1: Systematic Deduplication
    df = df.drop_duplicates()
    dedup_count = len(df)
    print(f"[Data Pipeline] Deduplication: {initial_count:,} -> {dedup_count:,} (-{initial_count - dedup_count:,} duplicate records)")
    print(f"[Data Pipeline] Total Frauds: {df['Class'].sum():,} ({df['Class'].mean()*100:.3f}% natural prevalence)")
    
    # Step 2: Separate features and target (exclude 'Time' to avoid time-index memorization)
    feature_cols = [c for c in df.columns if c not in ['Class', 'Time']]
    X = df[feature_cols]
    y = df['Class']
    
    # Step 3: Leakage-Free Stratified Partitioning
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"[Data Pipeline] Train partition: {len(X_train):,} samples ({y_train.sum()} frauds)")
    print(f"[Data Pipeline] Test partition:  {len(X_test):,} samples ({y_test.sum()} frauds)")
    
    # Step 4: Normalization fit strictly on Train partition
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return {
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "X_train_raw": X_train,
        "X_test_raw": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler,
        "feature_names": feature_cols
    }

