# IEEE-CIS Fraud Detection Benchmark Report
## Empirical Evaluation of 6 Machine Learning & Deep Learning Models on the Vesta / IEEE-CIS Dataset

**Dataset:** IEEE-CIS Fraud Detection Competition (`train_transaction.csv`)  
**Source:** Vesta Corporation / Kaggle Competition (2019)  
**Total Records:** 590,540 online transactions | 394 initial features  
**Fraud Cases:** 20,663 events (3.50% natural fraud prevalence)  
**Testing Split:** 24,000 held-out transactions (840 actual fraud cases, 23,160 legitimate)  
**Date:** Academic Year 2025–2026  

---

## 1. Full Empirical Benchmark Results Table

All 6 models were trained on the **exact same training partition** ($N = 96,000$) and evaluated on the **exact same held-out test partition** ($N = 24,000$):

```
+-------------------------------------------------------------------------------------------------------------------------------+
|                                    IEEE-CIS FRAUD DETECTION: MODEL COMPARISON TABLE                                           |
+----------------------------+--------------+---------------+------------+--------------+---------+---------+--------+----------+
| Model                      | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) | ROC-AUC | AUPRC   | FP     | FN       |
+----------------------------+--------------+---------------+------------+--------------+---------+---------+--------+----------+
| LightGBM                   | 97.74%       | 88.37%        | 40.71%     | 55.75%       | 0.9165  | 0.6131  | 45     | 498      |
| XGBoost (GBDT Ensemble)    | 97.71%       | 87.96%        | 40.00%     | 54.99%       | 0.9201  | 0.6203  | 46     | 504      |
| Random Forest (100 Trees)  | 97.47%       | 92.65%        | 30.00%     | 45.32%       | 0.8913  | 0.5524  | 20     | 588      |
| Decision Tree (CART)       | 97.19%       | 71.21%        | 32.98%     | 45.08%       | 0.8181  | 0.3815  | 112    | 563      |
| Deep Learning (Focal Loss) | 97.04%       | 77.92%        | 21.43%     | 33.61%       | 0.8619  | 0.4296  | 51     | 660      |
| Logistic Regression (L2)   | 96.90%       | 81.46%        | 14.64%     | 24.82%       | 0.8256  | 0.3309  | 28     | 717      |
+----------------------------+--------------+---------------+------------+--------------+---------+---------+--------+----------+
```

---

## 2. Key Insights for Your Project Guide

### 1. Who Has the Better Accuracy on IEEE-CIS?
* **Rank 1:** **LightGBM** achieved the highest accuracy at **97.74%** and the highest F1-Score (**55.75%**).
* **Rank 2:** **XGBoost** followed closely with **97.71% accuracy**, while achieving the **highest ROC-AUC (0.9201)** and **highest AUPRC (0.6203)** across all models.
* **Rank 3:** **Random Forest** achieved **97.47% accuracy** and the **highest precision at 92.65%** (only 20 false positives out of 24,000 transactions).

### 2. Cross-Dataset Comparison: ULB European Card vs. IEEE-CIS E-Commerce
Your project now contains a comparative analysis across **two distinct gold-standard datasets**:

| Experimental Dimension | ULB European Card Dataset | IEEE-CIS E-Commerce Dataset |
| :--- | :--- | :--- |
| **Data Topology** | 30 continuous PCA features | 394 raw, heterogeneous tabular features |
| **Fraud Prevalence** | 0.17% (Extreme Imbalance) | 3.50% (Moderate Skewness) |
| **Top Model by Accuracy** | Deep Learning with Focal Loss (**99.94%**) | LightGBM (**97.74%**) & XGBoost (**97.71%**) |
| **Top Model by ROC-AUC** | Random Forest (**0.9702**) | XGBoost (**0.9201**) |
| **Latency Budget** | $<1.0\text{ ms}$ on CPU | $0.8\text{--}1.2\text{ ms}$ on CPU |

### 3. Why GBDTs (XGBoost & LightGBM) Dominated IEEE-CIS:
Unlike the ULB dataset where features are pre-compressed with PCA, IEEE-CIS contains hundreds of raw, sparse e-commerce transaction indicators (`TransactionAmt`, `ProductCD`, `card1-card6`, `addr1/2`, `P_emaildomain`, `C-series`, `D-series`). Gradient Boosted Decision Trees naturally excel at handling tabular sparsity, missing values, and complex non-linear feature interactions without requiring extensive neural representation learning.
