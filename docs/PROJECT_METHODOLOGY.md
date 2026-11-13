# Final Year Project Methodology
## Multi-Tier Real-Time Financial Fraud Detection Framework with Class Imbalance Mitigation, Focal Loss, and Explainable AI (XAI)

**Academic Level:** Final Year Project (Bachelor of Engineering / Bachelor of Science / Master's Capstone)  
**Domain:** Artificial Intelligence, Financial Machine Learning, Cybersecurity  
**Prepared For:** Project Mentor & Academic Examination Panel  
**Date:** March 2026 / Academic Year 2025–2026  

---

## Executive Summary & Research Rationale

Financial fraud generates global economic losses exceeding hundreds of billions of dollars annually (over $400 billion in the US alone in 2022; *Yang et al., 2026*). While machine learning (ML) and artificial intelligence (AI) have become the gold standard for fraud prevention, conventional implementations in academic projects suffer from four critical deficiencies:
1. **The Accuracy Paradox & Metric Misalignment**: Relying on standard classification accuracy in datasets where fraud represents less than 0.2% of transactions yields deceptive results (a naive model predicting all transactions as legitimate achieves 99.83% accuracy while capturing 0% of fraud) (*Ali et al., 2022; Yang et al., 2026*).
2. **Single-Dataset & Resampling Bias**: Training solely on small or synthetic datasets leads to overfitting. Data-level oversampling (e.g., standard SMOTE) often synthesizes unrealistic samples in sparse decision spaces (*Albalawi & Dardouri, 2025*).
3. **Black-Box Opacity & Compliance Gaps**: High-performing deep neural networks and ensemble models cannot be adopted in banking and anti-money laundering (AML) operations without transparent, case-level justification satisfying regulatory compliance (*Hernandez Aros et al., 2024; Yang et al., 2026*).
4. **Latency Budget Neglect**: Transaction authorizations in modern payment switches must occur within strict millisecond thresholds ($<10\text{ ms}$), rendering complex unoptimized architectures infeasible for real-time deployment (*Albalawi & Dardouri, 2025*).

This project methodology addresses these challenges by proposing a **multi-tier, dual-validated, cost-sensitive, and explainable financial fraud detection system**.

---

## 1. Project Objectives & Research Questions

### 1.1 Research Questions (Guided by Kitchenham & PRISMA Protocols)
Following the systematic literature review (SLR) guidelines established by *Ali et al. (2022)*, *Yang et al. (2026)*, and *Hernandez Aros et al. (2024)*, this project addresses the following research questions:
- **RQ1**: How does algorithm-level imbalance handling (Focal Loss) compare against data-level resampling (SMOTE) across linear, tree-ensemble, and deep learning architectures?
- **RQ2**: Does the proposed framework maintain cross-domain generalizability when evaluated across real-world payment card data and simulated mobile money networks?
- **RQ3**: Can local and global Explainable AI (SHAP and LIME) provide auditable, feature-level justifications without sacrificing predictive precision?
- **RQ4**: How can a two-tier screening pipeline reconcile the trade-off between sub-second authorization latency ($<5\text{ ms}$) and deep forensic detection accuracy?

### 1.2 Core Project Deliverables
1. An automated, leakage-free data preprocessing and statistical verification pipeline.
2. A comparative evaluation matrix of 5 machine learning and deep learning models across two benchmark datasets.
3. An algorithm-level loss adaptation module implementing Binary Focal Loss.
4. An Explainable AI (XAI) auditing module producing SHAP waterfall charts for flagged transactions.
5. An operational two-tier real-time inference prototype with sub-10ms latency profiling.

---

## 2. Experimental Data Foundation (Dual-Dataset Strategy)

To avoid localized benchmark bias (*Albalawi & Dardouri, 2025*), this project adopts a dual-dataset design covering both card transactions and mobile wallet transfers:

```
+----------------------------------------------------------------------------------------------------+
|                                    DATASET SPECIFICATIONS & COMPARISON                             |
+-----------------------------+------------------------------------+---------------------------------+
| Attribute                   | Benchmark 1: ULB European Card     | Benchmark 2: PaySim Mobile      |
+-----------------------------+------------------------------------+---------------------------------+
| Source Domain               | European Cardholders (Kaggle)      | Mobile Money Transfer Simulator |
| Data Nature                 | Real-World Commercial Bank Records | Agent-Based Synthetic Simulator |
| Total Instances             | 284,807 transactions               | 6,362,620 transactions          |
| Fraudulent Instances        | 492 cases (0.172%)                 | 8,213 cases (0.129%)            |
| Feature Representation      | 28 PCA Components (V1–V28),        | 10 Tabular features: type,      |
|                             | Time, Amount                       | amount, old/new balances        |
| Key Research Value          | Standard industry gold-standard;   | Tests transaction-flow dynamics |
|                             | evaluate high-dimensional PCA      | and cross-domain robustness     |
+-----------------------------+------------------------------------+---------------------------------+
```

---

## 3. End-to-End System Architecture

```
                                  [ RAW TRANSACTION DATA ]
                       (ULB Credit Card: 284,807 | PaySim: 6.36M)
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │       PHASE 1: DATA QUALITY & INTEGRITY       │
                    │  • Duplicate Removal (284,807 -> 283,726)    │
                    │  • Null Audit (Verified 0 Missing Values)    │
                    │  • Statistical Profiling (Mann-Whitney U)    │
                    └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │    PHASE 2: LEAKAGE-FREE SPLIT & SCALING     │
                    │  • Stratified 80/20 Chronological Split      │
                    │  • Train: 80% (Preserve 0.17% class prior)   │
                    │  • Test: 20% (Pure unseen evaluation data)   │
                    │  • StandardScaler / RobustScaler fit on TRAIN│
                    └──────────────────────┬───────────────────────┘
                                            │
                        ┌───────────────────┴───────────────────┐
                        ▼                                       ▼
        ┌───────────────────────────────┐       ┌───────────────────────────────┐
        │   BRANCH A: DATA-LEVEL SMOTE  │       │  BRANCH B: ALGORITHM-LEVEL    │
        │  • Interpolate k=5 neighbors  │       │  • Preserve true distribution │
        │  • Applied ONLY to Train split│       │  • Binary Focal Loss (γ=2,α)  │
        │  • Balanced Train: 1:1 ratio  │       │  • Cost-Sensitive Weights     │
        └───────────────┬───────────────┘       └───────────────┬───────────────┘
                        │                                       │
                        ▼                                       ▼
        ┌───────────────────────────────┐       ┌───────────────────────────────┐
        │   CONVENTIONAL & ENSEMBLE ML  │       │      DEEP LEARNING MODEL      │
        │  • Logistic Regression (L2)   │       │  • 4-Layer Dense Architecture │
        │  • Decision Tree (CART)       │       │  • Batch Normalization + Drop │
        │  • Random Forest (100 trees)  │       │  • Focal Loss Optimization    │
        │  • XGBoost / LightGBM         │       │  • Early Stopping (Patience=5)│
        └───────────────┬───────────────┘       └───────────────┬───────────────┘
                        │                                       │
                        └───────────────────┬───────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │        PHASE 4: RIGOROUS EVALUATION          │
                    │  • Metrics: AUPRC, ROC-AUC, Precision, Recall│
                    │  • Domain Cost-Matrix: Financial Loss Saved  │
                    │  • 10-Fold Cross-Validation Paired t-tests   │
                    └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │   PHASE 5: EXPLAINABILITY & OPERATIONALIZATION│
                    │  • Global Feature Importance (TreeSHAP)      │
                    │  • Local Instance Explanations (SHAP/LIME)   │
                    │  • Two-Tier Deployment (<5ms Real-Time Gate) │
                    └──────────────────────────────────────────────┘
```

---

## 4. Phase-by-Phase Technical Methodology

### Phase 1: Data Preprocessing & Statistical Verification
1. **Deduplication**: 
   - Based on *Albalawi & Dardouri (2025)*, duplicate transactions must be eliminated to ensure models are trained and tested on strictly independent observations.
   - On the Kaggle dataset, deduplication reduces the volume from **284,807 to 283,726** (1,081 redundant records removed).
2. **Missing Value Audit**: 
   - Verify complete data integrity. Both ULB and PaySim benchmarks have 0 missing values.
3. **Statistical Hypothesis Testing (Mann-Whitney U Test)**:
   - Financial fraud amounts exhibit severe non-Gaussian distributions (*Albalawi & Dardouri, 2025*).
   - Formulate hypothesis:
     - $H_0$: The distribution of transaction amounts for fraudulent transactions is identical to legitimate transactions.
     - $H_1$: Fraudulent transaction amounts are significantly lower ($p < 0.05$).
   - Fraudsters systematically keep transaction amounts below $500 to evade automated heuristic thresholds, confirming `Amount` as a statistically significant discriminative feature.

---

### Phase 2: Feature Transformation & Leakage-Free Splitting
1. **Stratified Splitting**:
   - Split dataset into **80% Training ($N \approx 226,980$)** and **20% Testing ($N \approx 56,746$)**.
   - Use `StratifiedShuffleSplit` or temporal ordering (using the `Time` index) to maintain the exact 0.17% fraud prevalence in both splits.
2. **Scaling Without Leakage**:
   - To prevent data snooping/lookahead bias (*Yang et al., 2026*), standard scaling parameters ($\mu, \sigma$) must be computed strictly on the training partition:
     $$z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$$
   - Apply the fitted scaler to the held-out test partition.

---

### Phase 3: Class Imbalance Mitigation Strategy

This project compares the two prevailing paradigms identified in the literature:

#### Method 1: Synthetic Minority Over-Sampling Technique (SMOTE)
- *Technique*: Generates synthetic examples along the line segments joining any/all of the $k=5$ nearest minority neighbors in feature space (*Albalawi & Dardouri, 2025; Ali et al., 2022*):
  $$x_{\text{synthetic}} = x_i + \lambda \cdot (x_{zi} - x_i), \quad \lambda \sim U(0, 1)$$
- *Target Distribution*: Generates 226,110 synthetic fraud records, yielding a balanced 1:1 training ratio (226,602 fraud, 226,602 legitimate).
- *Strict Rule*: Resampling is applied **exclusively to the training split**. The testing split remains untouched at the natural 0.17% fraud rate.

#### Method 2: Algorithm-Level Binary Focal Loss
To prevent SMOTE from fabricating artifacts in high-dimensional sparse spaces (*Yang et al., 2026*), the deep learning model uses **Focal Loss**:
$$\mathcal{L}_{\text{Focal}} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$
Where:
- $p_t$ is the model's estimated probability for the true class.
- $\alpha_t = 0.25$ addresses class imbalance.
- $\gamma = 2.0$ dynamically suppresses loss contributions from easy, well-classified legitimate transactions, forcing backpropagation gradients to focus on ambiguous fraud boundaries.

---

### Phase 4: Model Implementation & Optimization

Five model categories are systematically implemented and tuned using 5-fold Stratified Cross-Validation and Grid Search:

```
+----------------------------------------------------------------------------------------------------+
|                                    MODEL HYPERPARAMETER SEARCH SPACE                               |
+-----------------------+------------------------------------+---------------------------------------+
| Model                 | Architecture / Estimator           | Tuned Hyperparameters                 |
+-----------------------+------------------------------------+---------------------------------------+
| Logistic Regression   | Generalized Linear Model           | C: [0.01, 0.1, 1.0, 10]               |
|                       | (L2 Regularized Baseline)          | Penalty: ['l1', 'l2'], Solver: liblin |
+-----------------------+------------------------------------+---------------------------------------+
| Decision Tree         | CART Classifier                    | Max Depth: [5, 10, 20, None]          |
|                       | (Interpretable Non-linear)         | Min Samples Split: [2, 5, 10]         |
|                       |                                    | Min Samples Leaf: [1, 2, 4]           |
+-----------------------+------------------------------------+---------------------------------------+
| Random Forest         | Bagging Ensemble                   | N Estimators: [50, 100, 200]          |
|                       | (Variance Reduction)               | Max Depth: [10, 20, None]             |
|                       |                                    | Min Samples Split: [2, 5]             |
+-----------------------+------------------------------------+---------------------------------------+
| XGBoost / LightGBM    | Gradient Boosted Decision Trees    | N Estimators: [50, 100, 150, 200]     |
|                       | (Sequential Error Correction)      | Max Depth: [3, 5, 7, 9]               |
|                       |                                    | Learning Rate: [0.01, 0.1, 0.2]       |
|                       |                                    | Subsample: [0.6, 0.8, 1.0]            |
+-----------------------+------------------------------------+---------------------------------------+
| Deep Neural Network   | Multi-Layer Perceptron (MLP)       | Layers: 4 (Dense 256 -> 128 -> 64 -> 1)|
| (Improved Focal DL)   | with Batch Normalization & Dropout | Dropout: [0.2, 0.3, 0.5]              |
|                       |                                    | Learning Rate: [0.001, 0.0005]        |
|                       |                                    | Batch Size: [32, 64]                  |
|                       |                                    | Optimizer: Adam; Loss: Focal Loss     |
+-----------------------+------------------------------------+---------------------------------------+
```

---

## 5. Performance Evaluation & Validation Framework

### 5.1 Metric Selection (Addressing the Accuracy Paradox)
As emphasized by *Kamuangu (2024)*, *Ali et al. (2022)*, and *Yang et al. (2026)*, reporting solely accuracy is invalid for imbalanced fraud. The evaluation suite comprises:

$$\text{Precision} = \frac{TP}{TP + FP} \quad \text{(Minimizes customer friction & false alarm costs)}$$

$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN} \quad \text{(Maximizes fraud interception & reduces dollar loss)}$$

$$F_1\text{-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \quad \text{(Harmonic equilibrium)}$$

$$\text{AUPRC} = \int_0^1 P(R) \, dR \quad \text{(Gold-standard metric under extreme skewness)}$$

$$\text{ROC-AUC} = \int_0^1 \text{TPR}(\text{FPR}) \, d(\text{FPR}) \quad \text{(Threshold-independent discrimination)}$$

### 5.2 Business-Driven Cost-Benefit Matrix
In real-world commercial banking, misclassification costs are highly asymmetrical (*Yang et al., 2026*):
- **Cost of False Negative ($C_{FN}$)**: Average fraudulent transaction amount + statutory chargeback investigation fee ($\approx \$150.00$).
- **Cost of False Positive ($C_{FP}$)**: Cost of automated SMS alert + customer service friction ($\approx \$3.00$).

The project computes the **Total Financial Operational Loss**:
$$\text{Financial Loss} = (C_{FN} \times FN) + (C_{FP} \times FP)$$
The model that minimizes this loss function represents the operationally optimal solution.

### 5.3 Statistical Significance Testing
To confirm performance improvements are not random variations (*Albalawi & Dardouri, 2025*):
- Run **10 independent cross-validation iterations**.
- Compute pairwise two-tailed Student's t-tests comparing the proposed Deep Learning model against baseline classifiers:
  $$t = \frac{\bar{d}}{\frac{s_d}{\sqrt{n}}}, \quad df = n - 1$$
- Reject null hypothesis $H_0$ if $p < 0.05$.

---

## 6. Literature Benchmarking Targets

To demonstrate that this FYP meets or exceeds state-of-the-art standards, results will be benchmarked against findings published in the reference papers:

```
+----------------------------------------------------------------------------------------------------+
|                         LITERATURE BENCHMARK PERFORMANCE TARGETS                                   |
+---------------------------+-------------------------+------------+-----------+----------+----------+
| Literature Study          | Model Architecture      | Accuracy   | Precision | Recall   | F1-Score |
+---------------------------+-------------------------+------------+-----------+----------+----------+
| Kamuangu (2024) [Table 1] | Logistic Regression     | 92.00%     | 89.00%    | 85.00%   | 87.00%   |
| Kamuangu (2024) [Table 1] | Decision Tree           | 94.00%     | 91.00%    | 88.00%   | 89.00%   |
| Kamuangu (2024) [Table 1] | Support Vector Machine  | 93.00%     | 90.00%    | 87.00%   | 88.00%   |
| Kamuangu (2024) [Table 4] | Gradient Boosting (GBM) | 97.00%     | 95.00%    | 93.00%   | 94.00%   |
| Albalawi (2025) [Table 3] | Random Forest + SMOTE   | 99.69%     | 59.26%    | 100.0%   | 74.42%   |
| Albalawi (2025) [Table 3] | XGBoost (Optimized)     | 99.93%     | 91.67%    | 95.00%   | 93.30%   |
| Albalawi (2025) [Table 3] | Focal Loss Deep Learning| 99.89%     | 80.00%    | 100.0%   | 88.89%   |
+---------------------------+-------------------------+------------+-----------+----------+----------+
```

---

## 7. Explainable AI (XAI) & Compliance Layer

Regulated financial institutions are legally mandated under European GDPR Article 22 and US Fair Credit Reporting directives to provide explanation rationales for adverse financial decisions (*Yang et al., 2026; Hernandez Aros et al., 2024*).

```
                      [ Flagged Transaction: Suspicious Score = 0.94 ]
                                            │
                                            ▼
                           ┌─────────────────────────────────┐
                           │      TreeSHAP / DeepSHAP        │
                           │   Calculate Shapley Values      │
                           └────────────────┬────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
     [ GLOBAL FEATURE IMPORTANCE ]                   [ LOCAL INSTANCE WATERFALL ]
  Ranks most discriminative features              Decomposes individual decision:
  across entire population:                       • Base value: E[f(x)] = 0.0017
  1. V14 (Principal component 14)                 • V14 = -6.82  ──► (+0.54 risk)
  2. V10 (Principal component 10)                 • V12 = -4.11  ──► (+0.26 risk)
  3. V12 (Principal component 12)                 • Amount = $380──► (+0.12 risk)
  4. Amount (Transaction value)                   • Output: P(Fraud) = 0.94 [BLOCK]
```

1. **TreeSHAP Implementation**: Integrated with Random Forest and XGBoost to generate global summary beeswarm plots and feature interaction charts.
2. **Local Instance Waterfall Cards**: Integrated into the operational dashboard to provide human investigators with clear, auditable explanations for each blocked transaction.

---

## 8. Real-Time Operational Deployment (Two-Tier Gateway)

To address the latency and throughput requirements identified in *Albalawi & Dardouri (2025)* and *Yang et al. (2026)*, the final prototype implements a **Two-Tier Screening Pipeline**:

```
[ Incoming Payment Request ]
             │
             ▼
┌───────────────────────────────┐
│     TIER 1: REAL-TIME GATE    │  ◄── Evaluated in < 2 ms (CPU)
│  LightGBM / XGBoost Model     │
└──────────────┬────────────────┘
               │
      ┌────────┴────────┐
      │ Score Analysis  │
      └────────┬────────┘
               ├── P(Fraud) < 0.15 ──► [ APPROVED IMMEDIATELY ]
               ├── P(Fraud) > 0.85 ──► [ BLOCKED IMMEDIATELY ]
               │
               └── 0.15 <= P(Fraud) <= 0.85 (Ambiguous Zone)
                         │
                         ▼
        ┌────────────────────────────────┐
        │   TIER 2: ASYNC FORENSIC QUEUE │  ◄── Evaluated in ~25 ms (GPU)
        │  • Deep Learning (Focal Loss)  │
        │  • Deep Autoencoder Anomaly    │
        │  • Automated SHAP Report       │
        └────────────────┬───────────────┘
                         │
                         ▼
             [ Compliance Review Portal ]
```

### Real-Time Latency Benchmark Targets (from Albalawi & Dardouri, 2025, Table 4):
- **Logistic Regression / Decision Tree**: $< 1\text{ ms}$ (CPU) — *Ultra-fast baseline*
- **Random Forest / XGBoost**: $3\text{--}10\text{ ms}$ (CPU) — *Ideal for Tier-1 real-time gateway*
- **Deep Learning (Focal Loss)**: $\approx 25\text{ ms}$ (GPU RTX 3060) — *Ideal for Tier-2 forensic audit*

---

## 9. Technology Stack & Implementation Tools

- **Programming Language**: Python 3.10+
- **Data Engineering**: Pandas, NumPy, SciPy (Mann-Whitney U testing)
- **Imbalance Handling**: `imbalanced-learn` (SMOTE, ADASYN, RandomUnderSampler)
- **Traditional & Ensemble ML**: Scikit-Learn, XGBoost, LightGBM
- **Deep Learning Architecture**: PyTorch / TensorFlow Keras (Custom Focal Loss layer)
- **Model Explainability**: SHAP (SHapley Additive exPlanations), LIME
- **Interactive Mentor Demonstration**: Streamlit web dashboard + FastAPI REST endpoint
- **Experimental Tracking**: Weights & Biases (W&B) / MLflow

---

## 10. Project Work Plan & Defense Timeline (Gantt Structure)

```
Week  1 -  2: Dataset ingestion, deduplication, missing value check, Mann-Whitney U test.
Week  3 -  4: Leakage-free train/test splitting, StandardScaler pipeline, SMOTE balancing.
Week  5 -  6: Baseline models (Logistic Regression, Decision Tree) + Tree Ensembles (RF, XGBoost).
Week  7 -  8: Deep Learning model with custom Focal Loss, Batch Normalization, and Dropout.
Week  9 - 10: Cross-domain validation on PaySim dataset; 10-fold paired t-tests.
Week 11 - 12: Explainable AI (SHAP & LIME) integration; cost-matrix curve analysis.
Week 13 - 14: Streamlit live demo development, latency benchmarking, final thesis compilation.
```

---

## 11. Academic References (Directly Synthesized from PDFs)

1. **Albalawi, T., & Dardouri, S. (2025).** Enhancing credit card fraud detection using traditional and deep learning models with class imbalance mitigation. *Frontiers in Artificial Intelligence*, 8:1643292. https://doi.org/10.3389/frai.2025.1643292
2. **Ali, A., Abd Razak, S., Othman, S. H., Eisa, T. A. E., Al-Dhaqm, A., Nasser, M., ... & Saif, A. (2022).** Financial fraud detection based on machine learning: A systematic literature review. *Applied Sciences*, 12(19), 9637. https://doi.org/10.3390/app12199637
3. **Hernandez Aros, L., Bustamante Molano, L. X., Gutierrez-Portela, F., Moreno Hernandez, J. J., & Rodríguez Barrero, M. S. (2024).** Financial fraud detection through the application of machine learning techniques: a literature review. *Humanities and Social Sciences Communications*, 11(1), 1130. https://doi.org/10.1057/s41599-024-03606-0
4. **Kamuangu, P. K. (2024).** A review on financial fraud detection using AI and machine learning. *Journal of Economics, Finance and Accounting Studies*, 6(1), 67-77. https://doi.org/10.32996/jefas.2024.6.1.7
5. **Yang, H., Shukur, Z., & Sahran, S. (2026).** A review of artificial intelligence for financial fraud detection. *Applied Sciences*, 16(4), 1931. https://doi.org/10.3390/app16041931
