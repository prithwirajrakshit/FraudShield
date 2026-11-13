# Final Year Project Methodology Chapter
## A Multi-Tier Real-Time Financial Fraud Detection Framework with Class Imbalance Mitigation, Focal Loss, and Explainable AI (XAI)

**Author:** Final Year Project Candidate  
**Target:** Project Mentor & Academic Review Committee  
**Structure:** Formatted according to the standard 4-step academic research methodology framework  

---

## Step 1: Explain Your Methodological Approach

### 1.1 Research Problem and Core Questions ("The What")
Financial fraud presents an escalating existential threat to the global economy, with total annual losses exceeding $400 billion in the United States alone (*Yang et al., 2026*). While artificial intelligence (AI) and machine learning (ML) have become the primary instruments for proactive fraud prevention, conventional academic and industrial detection pipelines suffer from four persistent structural failures:
1. **The Accuracy Paradox:** In real transaction streams, fraudulent occurrences represent a microscopic fraction of overall traffic (typically $<0.2\%$). Under this extreme class skewness, a trivial classifier predicting all transactions as genuine achieves 99.83% accuracy while failing to intercept a single fraudulent event (*Ali et al., 2022; Yang et al., 2026*).
2. **Resampling Noise and Single-Benchmark Overfitting:** Most published literature evaluates algorithms exclusively on a single benchmark (primarily the ULB European Credit Card dataset). Furthermore, researchers rely heavily on standard Synthetic Minority Over-sampling Technique (SMOTE), which often interpolates synthetic points across high-dimensional sparse spaces, introducing decision boundary distortions (*Albalawi & Dardouri, 2025*).
3. **Regulatory Non-Compliance and Model Opacity:** State-of-the-art ensemble and deep neural architectures function as opaque black boxes. In regulated banking jurisdictions, automated denial of financial services without case-level, human-verifiable justification violates statutory directives such as Article 22 of the European General Data Protection Regulation (GDPR) and the US Fair Credit Reporting Act (*Hernandez Aros et al., 2024; Yang et al., 2026*).
4. **Latency Budget Infeasibility:** High-throughput payment authorization switches require inference responses within strict millisecond thresholds ($<10\text{ ms}$). Complex, unoptimized deep networks cannot be deployed synchronously without causing transaction timeouts and severe customer friction (*Albalawi & Dardouri, 2025*).

To address these vulnerabilities, this quantitative experimental study investigates four formal Research Questions (RQs), formulated in accordance with the Kitchenham and PRISMA systematic literature review protocols (*Ali et al., 2022; Yang et al., 2026*):
- **RQ1 (Imbalance Mitigation):** How does algorithm-level loss adaptation (Binary Focal Loss) compare against data-level oversampling (SMOTE) across linear, tree-ensemble, and deep learning architectures in terms of Precision-Recall trade-offs?
- **RQ2 (Cross-Domain Robustness):** Can a financial fraud detection framework trained on credit card transaction records maintain its predictive efficacy when generalized to a mobile money transfer network (PaySim)?
- **RQ3 (Regulatory Explainability):** How can local and global Explainable AI (TreeSHAP and LIME) be integrated into complex ensemble and neural models to produce auditable, feature-level decision rationales for compliance officers?
- **RQ4 (Operational Feasibility):** Can a two-tier screening architecture decouple sub-5ms real-time transaction authorization from asynchronous deep forensic analysis without reducing overall fraud interception capacity?

### 1.2 Research Paradigm, Epistemological Rationale, and Validity Criteria ("The Why")
This investigation is situated within an **empirical, quantitative experimental research paradigm**. A quantitative methodology is strictly necessary because financial fraud detection relies on identifying subtle, non-linear separations and probabilistic anomalies across high-dimensional continuous and categorical feature spaces. Establishing these boundaries requires mathematically rigorous, controlled manipulation of data distributions, loss functions, and decision thresholds.

The methodology is designed to satisfy three foundational scientific criteria:
1. **Internal Validity (Elimination of Data Leakage):** A recurring flaw in fraud literature is applying normalization or oversampling across the entire dataset prior to splitting, which leaks future distribution parameters into the training process. In this methodology, all data partitioning is executed strictly prior to any transformation. Normalization scalers ($\mu_{\text{train}}, \sigma_{\text{train}}$) and synthetic resampling algorithms are fit exclusively on the training split and applied downstream to the test split.
2. **External Validity (Generalizability Across Financial Paradigms):** In accordance with recommendations by *Albalawi & Dardouri (2025)* and *Hernandez Aros et al. (2024)*, this study rejects the convention of evaluating models on a single dataset. By employing a dual-benchmark strategy combining real-world banking card transactions (Kaggle) with agent-based mobile money simulations (PaySim), the framework proves generalizability across distinct financial products, currency flows, and transaction topologies.
3. **Reliability and Replicability:** To eliminate random variation in model performance, all experiments are validated using 10-fold Stratified Cross-Validation. Differences in model metrics are evaluated for statistical significance using pairwise two-tailed Student's t-tests with a significance threshold of $p < 0.05$ (*Albalawi & Dardouri, 2025*).

### 1.3 Prevention of Research Bias
The experimental protocol explicitly guards against common forms of statistical and methodological bias:
- **Sampling and Undercoverage Bias:** Preserved by maintaining the natural, unadulterated fraud prevalence ($0.172\%$ and $0.129\%$) in all held-out testing partitions, rather than evaluating on artificially balanced 50:50 test sets.
- **Information and Redundancy Bias:** Mitigated by conducting systematic deduplication, removing 1,081 redundant records from the primary dataset to ensure all observations are independent (*Albalawi & Dardouri, 2025*).
- **Omitted Variable Bias:** Addressed by combining temporal interval tracking, non-linear PCA behavioral components, and raw transaction volumes.

### 1.4 Ethical and Data Governance Considerations
Financial transaction research involves sensitive corporate and individual records. To uphold institutional research ethics, this project utilizes publicly accessible, fully anonymized secondary datasets:
- The ULB dataset replaces confidential account details with 28 Principal Component Analysis (PCA) orthogonal vectors, guaranteeing zero disclosure of Personally Identifiable Information (PII) (*Machine Learning Group, 2018*).
- The PaySim dataset is synthetically generated via multi-agent simulations calibrated on aggregated macro-statistics from an African mobile money operator, fully protecting customer identity while maintaining behavioral fidelity (*López-Rojas, 2017*).

---

## Step 2: Describe Your Data Collection Methods

### 2.1 Selection of Secondary Experimental Data Sources
Primary data collection via commercial banking APIs was precluded due to banking secrecy laws, non-disclosure agreements, and customer privacy mandates. Consequently, high-fidelity secondary benchmarks were acquired based on strict inclusion and exclusion criteria synthesized from systematic surveys (*Ali et al., 2022; Hernandez Aros et al., 2024*):

#### Dataset Inclusion & Exclusion Protocol:
- **Inclusion Criteria:**
  1. Publicly accessible, peer-reviewed financial transaction corpora with verified, ground-truth binary labels.
  2. Transaction volumes exceeding $100,000$ records to simulate industrial big-data scale.
  3. Realistic, natural class imbalance ($< 1\%$ positive fraud prevalence).
  4. Inclusion of raw transaction monetary values and temporal sequencing identifiers.
- **Exclusion Criteria:**
  1. Datasets older than 15 years (e.g., 1994 Statlog German Credit and Australian Credit Approval datasets), which *Hernandez Aros et al. (2024)* demonstrated are obsolete and unrepresentative of contemporary digital payment tactics.
  2. Proprietary datasets lacking public accessibility, which compromises academic replicability.
  3. Datasets lacking clear definitions of what constitutes a fraudulent event.

### 2.2 Operationalization of Variables & Dataset Schemas

#### Benchmark 1: ULB European Credit Card Transaction Dataset
- **Origin & Provenance:** Sourced from the Machine Learning Group at Université Libre de Bruxelles (ULB) via Kaggle (*Machine Learning Group, 2018; Albalawi & Dardouri, 2025*). Contains genuine card transactions completed by European cardholders over a 48-hour recording window in September 2013.
- **Sample Size & Class Balance:** $N = 284,807$ transactions, containing $492$ fraudulent events ($0.172\%$ positive class prevalence).
- **Operationalization of Attributes:**
  - `V1` through `V28`: Continuous numerical features obtained via Principal Component Analysis (PCA) transformation to safeguard customer confidentiality. These capture latent behavioral patterns (e.g., purchasing categories, velocity, terminal interactions).
  - `Time`: Continuous integer tracking elapsed seconds from the first recorded transaction; utilized for chronological ordering and drift analysis.
  - `Amount`: Continuous transaction value in Euros ($€$), ranging from $€0.00$ to $€25,691.16$.
  - `Class` (Target Variable): Binary ground-truth indicator, operationalized as $Y \in \{0, 1\}$, where $1$ denotes confirmed fraudulent activity and $0$ denotes legitimate commerce.

#### Benchmark 2: PaySim Mobile Money Financial Dataset
- **Origin & Provenance:** Developed by Edgar Lopez-Rojas (2017) using an agent-based financial simulator calibrated on real, anonymized transactional logs provided by a multinational mobile financial service provider operating across 14 countries (*López-Rojas, 2017; Albalawi & Dardouri, 2025*).
- **Sample Size & Class Balance:** $N = 6,362,620$ transactions, containing $8,213$ fraudulent events ($0.129\%$ positive class prevalence).
- **Operationalization of Attributes:**
  - `step`: Discrete temporal unit mapping chronological hours ($1 \text{ step} = 1 \text{ hour}$; 744 total steps simulating a 31-day operational month).
  - `type`: Categorical transaction modality operationalized into 5 distinct channels: `CASH-IN`, `CASH-OUT`, `DEBIT`, `PAYMENT`, and `TRANSFER`.
  - `amount`: Continuous monetary volume in local currency units.
  - `nameOrig` & `nameDest`: Unique cryptographic identifier strings representing transaction sender and recipient entities.
  - `oldbalanceOrg` & `newbalanceOrig`: Continuous numerical floats tracking customer balance immediately before and after transaction execution.
  - `oldbalanceDest` & `newbalanceDest`: Continuous numerical floats tracking recipient balance dynamics.
  - `isFraud` (Target Variable): Binary ground-truth label, where $1$ denotes fraudulent financial transfer/cash-out and $0$ denotes legitimate behavior.

---

## Step 3: Describe Your Analysis Method

### 3.1 Data Preparation and Preprocessing Pipeline
To guarantee data cleanliness and prevent experimental contamination, data preparation proceeds through four sequential phases (*Albalawi & Dardouri, 2025*):

1. **Systematic Deduplication:**
   An audit of the raw ULB dataset identified 1,081 duplicate transaction rows sharing identical PCA coordinates, amounts, and timestamps. These duplicate records were eliminated, reducing the analytical corpus from **284,807 to 283,726** unique transactions. This step guarantees that model validation is conducted on strictly independent observations.
2. **Missing Value Audit:**
   A programmatic null-value audit verified 0 missing, NaN, or corrupted values across both datasets, eliminating the need for synthetic data imputation.
3. **Leakage-Free Partitioning:**
   The deduplicated data is partitioned into an **80% Training Set ($N \approx 226,980$)** and a **20% Held-Out Testing Set ($N \approx 56,746$)** using Stratified Partitioning (and chronological verification using `Time`). Stratification ensures the exact $0.172\%$ operational fraud prevalence is preserved in both sets.
4. **Feature Normalization Without Lookahead Bias:**
   Because `Amount` and `Time` exhibit significant variance and heavy-tailed non-Gaussian distributions, features are standardized using `StandardScaler` (or `RobustScaler` for outlier resilience). The parameters are fit exclusively on the training partition:
   $$\mu_{\text{train}} = \frac{1}{N_{\text{train}}} \sum_{i=1}^{N_{\text{train}}} x_i, \quad \sigma_{\text{train}} = \sqrt{\frac{1}{N_{\text{train}}} \sum_{i=1}^{N_{\text{train}}} (x_i - \mu_{\text{train}})^2}$$
   $$z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$$
5. **Statistical Verification of Discriminability (Mann-Whitney U Test):**
   Following *Albalawi & Dardouri (2025)*, a non-parametric Mann-Whitney U test is executed on `Amount` between fraudulent and legitimate classes:
   $$U = n_1 n_2 + \frac{n_1(n_1 + 1)}{2} - R_1$$
   The test yields a statistically significant difference ($p < 0.05$), validating that fraudsters intentionally concentrate transactions in smaller monetary amounts ($< \$500$) to evade heuristic rule triggers.

### 3.2 Class Imbalance Mitigation Strategy
The analytical framework benchmarks two competing paradigms:

```
+----------------------------------------------------------------------------------------------------+
|                                    CLASS IMBALANCE MITIGATION STRATEGIES                           |
+--------------------------+-------------------------------------+-----------------------------------+
| Parameter                | Branch A: Data-Level SMOTE          | Branch B: Algorithm-Level Focal   |
+--------------------------+-------------------------------------+-----------------------------------+
| Mechanism                | Feature-space interpolation (k=5)   | Dynamic loss gradient attenuation |
| Application Point        | Training partition ONLY             | Backpropagation loss function     |
| Training Class Ratio     | Balanced 1:1 (226,602 : 226,602)    | Native skewed ratio (0.17% fraud) |
| Mathematical Formulation | x_new = x_i + λ(x_zi - x_i)         | FL(p_t) = -α_t(1 - p_t)^γ log(p_t)|
| Hyperparameters          | k = 5, sampling_strategy = 1.0      | γ = 2.0 (focusing), α = 0.25      |
| Primary Advantage        | Enhances decision boundary recall   | Prevents synthetic noise artifacts|
+--------------------------+-------------------------------------+-----------------------------------+
```

### 3.3 Model Portfolio & Hyperparameter Optimization
Five distinct algorithmic families are evaluated using 5-fold Stratified Cross-Validation combined with exhaustive Grid Search:

1. **Logistic Regression (L2 Baseline):** Generalized linear model optimized with `liblinear` solver and inverse regularization $C \in [0.01, 0.1, 1.0, 10]$.
2. **Decision Tree (CART):** Non-parametric tree classifier with `max_depth` $\in [5, 10, 20, \text{None}]$ and `min_samples_split` $\in [2, 5, 10]$.
3. **Random Forest:** Bagging ensemble of 100 decision trees utilizing bootstrap aggregation and feature subset randomization (`max_depth` $\in [10, 20]$, `max_features='sqrt'`).
4. **XGBoost / LightGBM:** Sequential gradient boosting correcting residual errors of weak trees (`n_estimators` $\in [100, 200]$, `learning_rate` $\in [0.01, 0.1]$, `max_depth` $\in [3, 6, 9]$).
5. **Deep Neural Network with Focal Loss (Proposed Model):** A 4-layer fully connected architecture engineered as follows:
   $$\text{Input}(30) \longrightarrow \text{Dense}(256, \text{ReLU}) \longrightarrow \text{BatchNorm} \longrightarrow \text{Dropout}(0.3)$$
   $$\longrightarrow \text{Dense}(128, \text{ReLU}) \longrightarrow \text{BatchNorm} \longrightarrow \text{Dropout}(0.3)$$
   $$\longrightarrow \text{Dense}(64, \text{ReLU}) \longrightarrow \text{BatchNorm} \longrightarrow \text{Dropout}(0.2)$$
   $$\longrightarrow \text{Dense}(1, \text{Sigmoid}) \longrightarrow P(\text{Fraud}) \in [0, 1]$$
   - Optimizer: Adam ($\eta = 0.001$, $\beta_1 = 0.9$, $\beta_2 = 0.999$).
   - Regularization: EarlyStopping (`monitor='val_loss'`, `patience=5`), `ReduceLROnPlateau(factor=0.5)`.
6. **Deep Autoencoder (Unsupervised Benchmark):** Encoder-decoder bottleneck network trained exclusively on legitimate transactions to identify zero-day attacks via reconstruction error thresholds (*Kamuangu, 2024*).

### 3.4 Software & Computational Environment
- **Core Environment:** Python 3.10+, NumPy, Pandas, SciPy.
- **Machine Learning & Resampling:** Scikit-Learn, `imbalanced-learn`, XGBoost, LightGBM.
- **Deep Learning Framework:** PyTorch / TensorFlow Keras.
- **Explainability Suite:** SHAP (SHapley Additive exPlanations), LIME.
- **Hardware Platform:** Intel Core i7 CPU, 16GB System RAM, NVIDIA GeForce RTX 3060 GPU (CUDA 12.x enabled).

### 3.5 Performance Evaluation & Cost-Sensitive Analytics

#### 1. Core Classification Metrics:
To eliminate the accuracy paradox, primary evaluation relies on:
- **Precision:** $\frac{TP}{TP + FP}$ (Minimizes false alarms and investigator overhead).
- **Recall (Sensitivity):** $\frac{TP}{TP + FN}$ (Maximizes fraud dollar capture).
- **F1-Score:** $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ (Harmonic balance).
- **AUPRC (Area Under Precision-Recall Curve):** Primary metric for imbalanced classification (*Yang et al., 2026; Saito & Rehmsmeier, 2015*).
- **ROC-AUC:** Area under the True Positive Rate vs. False Positive Rate curve.

#### 2. Domain-Specific Asymmetric Cost Matrix:
Operational effectiveness is evaluated using a commercial banking loss equation (*Yang et al., 2026*):
$$\text{Total Operational Financial Loss} = (C_{FN} \times FN) + (C_{FP} \times FP)$$
Where:
- $C_{FN} = \$150.00$: Average financial loss of missed fraud plus chargeback processing fees.
- $C_{FP} = \$3.00$: Cost of automated customer SMS notification and friction verification.

#### 3. Statistical Significance Testing:
All metrics are recorded across 10 independent stratified runs ($n = 10$). Pairwise two-tailed Student's t-tests are executed comparing the proposed Deep Learning model against baseline classifiers (*Albalawi & Dardouri, 2025*):
$$t = \frac{\bar{d}}{\frac{s_d}{\sqrt{n}}}, \quad df = n - 1$$
Null hypothesis $H_0$ is rejected if $p < 0.05$.

---

## Step 4: Evaluate and Justify the Methodological Choices You Made

### 4.1 Justification of Key Methodological Decisions

#### 1. Why Dual Datasets (Kaggle Credit Card + PaySim Mobile Money)?
*Justification:* Systematic reviews by *Hernandez Aros et al. (2024)* and *Yang et al. (2026)* revealed that over 70% of published academic fraud detection papers rely solely on the Kaggle credit card dataset. This creates severe dataset-specific bias, where models inadvertently memorize PCA artifacts that do not exist in other banking protocols. Incorporating the PaySim mobile money dataset allows testing across multi-step peer-to-peer transfers, balance shifts, and cash-out schemes. Demonstrating high performance across both benchmarks validates the true external generalizability of the proposed framework.

#### 2. Why Algorithm-Level Focal Loss over Pure Data-Level SMOTE?
*Justification:* While SMOTE is widely used, *Yang et al. (2026)* and *Albalawi & Dardouri (2025)* demonstrated that linear interpolation in high-dimensional sparse spaces frequently synthesizes unrealistic fraud instances within legitimate feature clusters, causing high false-positive rates (observed in *Albalawi's* Random Forest achieving only 59.26% precision). Focal Loss dynamically adjusts gradients during backpropagation, heavily down-weighting easy legitimate transactions and concentrating model capacity on hard borderline fraud cases without corrupting the native data distribution.

#### 3. Why a Two-Tier Screening Architecture?
*Justification:* In real-world payment networks, authorization engines must return a decision within $<10\text{ ms}$. Complex deep networks and autoencoders require $\approx 25\text{ ms}$ on GPU hardware (*Albalawi & Dardouri, 2025, Table 4*), making them impossible to run synchronously on every incoming authorization request. The proposed Two-Tier Architecture resolves this operational conflict:
- **Tier 1 (Real-Time Gate):** A lightweight LightGBM classifier executes on standard CPUs in $<2\text{ ms}$. Confident legitimate transactions ($P < 0.15$) are approved immediately; extreme fraud cases ($P > 0.85$) are blocked immediately.
- **Tier 2 (Asynchronous Forensic Queue):** Ambiguous transactions ($0.15 \le P \le 0.85$, representing $<3\%$ of traffic) are routed to the GPU-accelerated Deep Focal Network, Autoencoder, and automated SHAP explainer for forensic review.

#### 4. Why Integrate SHAP & LIME (Explainable AI)?
*Justification:* Financial institutions cannot deploy opaque models due to regulatory requirements (e.g., GDPR Article 22, US Equal Credit Opportunity Act). TreeSHAP provides mathematically rigorous Shapley feature attributions, enabling human compliance officers to inspect individual waterfall cards (e.g., confirming a transaction was blocked specifically because component $V_{14} < -6.8$ and $Amount = \$420$) rather than relying on uninterpretable probability scores (*Yang et al., 2026*).

### 4.2 Methodological Strengths vs. Limitations

```
+----------------------------------------------------------------------------------------------------+
|                                 STRENGTHS VS. LIMITATIONS EVALUATION                               |
+------------------------------------+---------------------------------------------------------------+
| Methodological Dimension           | Analytical Evaluation & Trade-Off Justification               |
+------------------------------------+---------------------------------------------------------------+
| Feature Anonymization (Kaggle)     | LIMITATION: PCA transformation obscures raw semantic features.|
|                                    | JUSTIFICATION: Guarantees full data privacy; supplemented by  |
|                                    | PaySim which provides unmasked, interpretable balance flows.  |
+------------------------------------+---------------------------------------------------------------+
| Temporal Depth & Concept Drift     | LIMITATION: Kaggle spans 48 hours, restricting drift study.   |
|                                    | JUSTIFICATION: Mitigated by PaySim's 31-day temporal steps   |
|                                    | and strict non-shuffled chronological train/test partitioning.|
+------------------------------------+---------------------------------------------------------------+
| Computational Hardware Demands     | LIMITATION: Deep learning models require GPU acceleration.     |
|                                    | JUSTIFICATION: Outweighed by Tier-1 CPU screening gateway,   |
|                                    | ensuring high-throughput feasibility on commodity hardware.   |
+------------------------------------+---------------------------------------------------------------+
| Trade-Off between Precision/Recall | LIMITATION: Maximizing recall can elevate false alarms.       |
|                                    | JUSTIFICATION: Resolved by implementing an asymmetric banking |
|                                    | cost function ($150 FN vs $3 FP) to optimize economic loss.   |
+------------------------------------+---------------------------------------------------------------+
```

---

## Academic References (Synthesized from Provided Literature)

1. **Albalawi, T., & Dardouri, S. (2025).** Enhancing credit card fraud detection using traditional and deep learning models with class imbalance mitigation. *Frontiers in Artificial Intelligence*, 8:1643292. https://doi.org/10.3389/frai.2025.1643292
2. **Ali, A., Abd Razak, S., Othman, S. H., Eisa, T. A. E., Al-Dhaqm, A., Nasser, M., ... & Saif, A. (2022).** Financial fraud detection based on machine learning: A systematic literature review. *Applied Sciences*, 12(19), 9637. https://doi.org/10.3390/app12199637
3. **Hernandez Aros, L., Bustamante Molano, L. X., Gutierrez-Portela, F., Moreno Hernandez, J. J., & Rodríguez Barrero, M. S. (2024).** Financial fraud detection through the application of machine learning techniques: a literature review. *Humanities and Social Sciences Communications (Nature Springer)*, 11(1), 1130. https://doi.org/10.1057/s41599-024-03606-0
4. **Kamuangu, P. K. (2024).** A review on financial fraud detection using AI and machine learning. *Journal of Economics, Finance and Accounting Studies*, 6(1), 67-77. https://doi.org/10.32996/jefas.2024.6.1.7
5. **Yang, H., Shukur, Z., & Sahran, S. (2026).** A review of artificial intelligence for financial fraud detection. *Applied Sciences*, 16(4), 1931. https://doi.org/10.3390/app16041931
6. **López-Rojas, E. (2017).** Synthetic financial datasets for fraud detection (PaySim). *Kaggle*. https://www.kaggle.com/datasets/ealaxi/paysim1
7. **Machine Learning Group - ULB. (2018).** Credit card fraud detection dataset. *Kaggle*. https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
8. **Saito, T., & Rehmsmeier, M. (2015).** The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE*, 10(3), e0118432. https://doi.org/10.1371/journal.pone.0118432
