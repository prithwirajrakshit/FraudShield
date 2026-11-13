# FraudShield • Real-Time Payment Fraud Security

A modern full-stack financial cybersecurity application that provides real-time fraud prevention and bank statement anomaly detection. Powered by a **PyTorch Deep Neural Network with Binary Focal Loss** and presented through a consumer-ready **React / Next.js 16 + Tailwind CSS** dashboard.

---

## Architecture Overview

```
 [ Consumer / Business User ]
              │
              ▼
 ┌────────────────────────────────────────────────────────┐
 │            NEXT.JS 16 + TAILWIND CSS FRONTEND          │
 │  • Port: http://localhost:3000                         │
 │  • Live Transaction Simulator Form                     │
 │  • Animated Radial Risk Gauge (0% – 100%)              │
 │  • Plain-English Audit & Action Cards (GDPR Art. 22)   │
 │  • CSV Bank Statement Drag-and-Drop Scanner            │
 └───────────────────────────┬────────────────────────────┘
                             │  HTTP POST /api/check-transaction (JSON)
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                 FASTAPI AI BACKEND SERVICE             │
 │  • Port: http://127.0.0.1:8000                         │
 │  • Validates payload with Pydantic                     │
 │  • Feature Mapping Engine (translates consumer fields) │
 │  • Normalizes inputs using models/scaler.joblib        │
 │  • Runs PyTorch inference (models/best_focal_dnn.pt)   │
 │  • Generates plain-English explanation reasons         │
 └────────────────────────────────────────────────────────┘
```

---

## How to Run

### Option 1: One-Click Launch (Starts Backend + Frontend)
Double-click `start.bat`, or execute in PowerShell:
```powershell
.\start.bat
```
*(Or run `.\scripts\start_app.ps1`)*
This opens two independent terminal windows:
1. **Backend**: FastAPI running at `http://127.0.0.1:8000`
2. **Frontend**: Next.js running at `http://localhost:3000`

---

### Option 2: Run Mobile App (Expo Go)
Double-click `scripts\run_mobile.bat`, or execute in PowerShell:
```powershell
.\scripts\run_mobile.ps1
```

---

### Option 3: Run Separately in Terminals

#### Terminal 1 — Backend (FastAPI):
```powershell
.\scripts\run_backend.ps1
```
*(Or manually):*
```powershell
& "C:\Users\praks\AppData\Local\Programs\Python\Python312\python.exe" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 — Frontend (Next.js):
```powershell
.\scripts\run_frontend.ps1
```
*(Or manually):*
```powershell
cd frontend
npm run dev
```

Once running, navigate to **[http://localhost:3000](http://localhost:3000)** in any browser.

---

## Core Application Capabilities

### 1. Live Transaction Guard (Single Check)
- **Human-Friendly Fields**: Enter Amount (₹), Merchant Name, Category (Dining, Grocery, Electronics, Crypto, Luxury, Travel, etc.), Channel (Chip & PIN, Contactless, Online, ATM).
- **Contextual Anomaly Toggles**: Cross-border foreign origin, off-peak night hours (1 AM – 5 AM), trusted device status.
- **Cardholder Spending Profile**: Adjustable typical average spend baseline.
- **Radial Risk Gauge**:
  - `0% - 30%` (🟢 Green): **APPROVED** (Safe purchase, cleared instantly).
  - `31% - 70%` (🟡 Amber): **CHALLENGE** (Suspicious activity, 2FA SMS passcode required).
  - `71% - 100%` (🔴 Red): **BLOCKED** (High-risk unauthorized attack, card guarded).
- **Explainable AI (XAI)**:
  - Bullet-point breakdown of key risk factors (e.g. *"Amount is 8.4x higher than usual average"*, *"Unrecognized device fingerprint"*).
  - Positive security alignments (e.g. *"Domestic region verified"*).
  - Clear recommended action steps for the consumer.

### 2. Universal Bank Statement Security Scanner
- **Any Bank Supported**: Uses an adaptive parser with 100+ fuzzy column aliases (SBI, HDFC, ICICI, Axis, Kotak Mahindra, PNB, BOB, Canara, Union, Chase, Revolut, etc.).
- **Multiple Formats**: Drag-and-drop or select bank statements in `.xlsx`, `.xls`, `.csv`, `.zip`, or `.pdf`.
- **Password-Protected Decryption**: Secure, local, in-memory unlocking for password-protected statements using `msoffcrypto`, `pyzipper`, and `pypdf`.
- **Privacy-by-Design**: 100% ephemeral in-memory processing. Zero database storage or disk logging of customer account data.
- **Click "Load Demo Statement"** to immediately test with pre-configured transactions (`data/sample_statement.csv`).
- **Telemetry & Summary Cards (₹ INR)**:
  - Total Scanned Transactions & Volume (₹)
  - Clear breakdown: Approved, Challenged (OTP verification), Blocked (Fraud attack)
  - Total Flagged / Guarded Capital Volume
  - Overall Account Security Health ("Healthy", "Review Needed", "At Risk")
- **Telemetry Audit Feed**: Interactive data table highlighting high-risk charges with color-coded risk tier badges and plain-English anomaly reasons.

---

## Project Structure

```
d:/Fraud Detection/
├── backend/
│   ├── main.py                     # FastAPI application & REST endpoints
│   └── services/
│       ├── feature_mapper.py       # Maps consumer inputs to 29-feature PCA space
│       ├── predictor.py            # Loads PyTorch FraudDNN & computes risk score
│       ├── explainer.py            # Generates plain-English reasons & advice
│       └── statement_scanner.py    # Multi-transaction statement parser
│
├── frontend/
│   ├── package.json
│   ├── postcss.config.mjs
│   └── src/
│       ├── app/
│       │   ├── layout.tsx          # Root HTML & metadata
│       │   ├── page.tsx            # Full-stack UI integration
│       │   └── globals.css         # Tailwind CSS styling
│       ├── components/
│       │   ├── Navbar.tsx          # FinTech branding & active protection badge
│       │   ├── RiskGauge.tsx       # Animated circular SVG gauge
│       │   ├── TransactionForm.tsx # Input simulator with preset scenarios
│       │   ├── ExplanationCard.tsx # Plain-English decision justification
│       │   └── StatementScanner.tsx# CSV upload, KPI cards, and anomaly table
│       └── lib/
│           └── api.ts              # Type-safe API client & fallback evaluator
│
├── mobile/                         # React Native + Expo Native Mobile Application
│   ├── App.tsx                     # Main app root & bottom navigation tabs
│   ├── app.json                    # Expo project configuration & Android package
│   └── src/
│       ├── components/
│       │   ├── Navbar.tsx          # Mobile header & live backend status
│       │   ├── RiskGauge.tsx       # Native SVG circular HUD threat gauge
│       │   ├── TransactionScreen.tsx# Mobile live payment simulation & GDPR XAI
│       │   ├── StatementScreen.tsx # Mobile Universal Bank Statement Scanner
│       │   └── ServerConfigModal.tsx# In-app Wi-Fi / LAN IP switcher modal
│       ├── lib/
│       │   └── api.ts              # Mobile REST client & local fallback engine
│       └── styles/
│           └── theme.ts            # Cyber-Obsidian theme constants
│
├── models/
│   ├── best_focal_dnn.pt           # Trained PyTorch neural network weights
│   ├── scaler.joblib               # StandardScaler fitted on training partition
│   └── metrics.json                # Empirical evaluation metrics
│
├── data/
│   └── sample_statement.csv        # Pre-configured statement for quick testing
│
├── docs/                           # Academic papers, UEM final project report & Viva guides
├── reports/                        # Report generator scripts, activity diagrams & logos
├── benchmarks/                     # IEEE-CIS & ULB credit card benchmark test suites
├── scripts/                        # Launcher scripts for backend, frontend & mobile
├── legacy/                         # Prototype Streamlit app (app.py)
│
├── start.bat                       # 1-Click Master Launcher for all services
└── README.md
```
