export interface TransactionCheckRequest {
  amount: number;
  merchant_name?: string;
  merchant_category: string;
  channel: string;
  is_foreign: boolean;
  is_night_time: boolean;
  device_trusted: boolean;
  user_avg_amount: number;
  velocity_1h: number;
}

export interface SecurityAssessment {
  fraud_probability: number;
  risk_score_percent: number;
  status: "APPROVED" | "CHALLENGE" | "BLOCKED";
  risk_tier: "Safe" | "Suspicious" | "High Risk";
  theme: "success" | "warning" | "danger";
  headline: string;
  latency_ms: number;
}

export interface RiskFactor {
  type: "critical" | "warning";
  title: string;
  detail: string;
}

export interface RecommendedAction {
  title: string;
  summary: string;
  steps: string[];
}

export interface TransactionCheckResponse {
  transaction_details: {
    amount: number;
    merchant_name?: string;
    category: string;
    channel: string;
  };
  security_assessment: SecurityAssessment;
  explanation: {
    risk_factors: RiskFactor[];
    safety_factors: string[];
    recommended_action: RecommendedAction;
  };
}

export interface Scenario {
  id: string;
  name: string;
  description: string;
  data: TransactionCheckRequest;
}

export interface ScannedTransaction {
  id: number;
  date: string;
  description: string;
  category: string;
  amount: number;
  risk_score_percent: number;
  status: "APPROVED" | "CHALLENGE" | "BLOCKED";
  risk_tier: string;
  theme: string;
  top_reason: string;
}

export interface StatementScanResponse {
  summary: {
    total_transactions: number;
    approved_count: number;
    challenged_count: number;
    blocked_count: number;
    total_volume_dollars: number;
    flagged_volume_dollars: number;
    account_health: string;
  };
  transactions: ScannedTransaction[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function checkTransaction(req: TransactionCheckRequest): Promise<TransactionCheckResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/check-transaction`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.warn("Backend unavailable, using client-side fallback evaluator:", err);
    return fallbackEvaluate(req);
  }
}

export async function fetchScenarios(): Promise<Scenario[]> {
  try {
    const res = await fetch(`${API_BASE}/api/scenarios`);
    if (res.ok) return await res.json();
  } catch (e) {
    // fallback scenarios
  }
  return [
    {
      id: "coffee",
      name: "Morning Coffee Purchase",
      description: "₹4.50 at a local cafe during normal morning commute",
      data: {
        amount: 4.5,
        merchant_name: "Corner Bakery & Coffee",
        merchant_category: "dining",
        channel: "contactless",
        is_foreign: false,
        is_night_time: false,
        device_trusted: true,
        user_avg_amount: 40.0,
        velocity_1h: 1,
      },
    },
    {
      id: "groceries",
      name: "Supermarket Groceries",
      description: "₹86.20 domestic in-store card purchase",
      data: {
        amount: 86.2,
        merchant_name: "Whole Foods Market",
        merchant_category: "grocery",
        channel: "in_store_chip",
        is_foreign: false,
        is_night_time: false,
        device_trusted: true,
        user_avg_amount: 50.0,
        velocity_1h: 1,
      },
    },
    {
      id: "electronics_new_device",
      name: "High-Value Gadget on New Device",
      description: "₹890.00 online laptop order from a newly detected browser",
      data: {
        amount: 890.0,
        merchant_name: "Apex Electronics Online",
        merchant_category: "electronics",
        channel: "online",
        is_foreign: false,
        is_night_time: false,
        device_trusted: false,
        user_avg_amount: 60.0,
        velocity_1h: 2,
      },
    },
    {
      id: "midnight_crypto",
      name: "Midnight Foreign Crypto Transfer",
      description: "₹2,450.00 transfer at 3:15 AM from an overseas IP gateway",
      data: {
        amount: 2450.0,
        merchant_name: "Global Crypto Vault Ltd",
        merchant_category: "crypto",
        channel: "online",
        is_foreign: true,
        is_night_time: true,
        device_trusted: false,
        user_avg_amount: 45.0,
        velocity_1h: 4,
      },
    },
  ];
}

export async function uploadStatement(file: File, password?: string): Promise<StatementScanResponse> {
  const formData = new FormData();
  formData.append("file", file);
  if (password && password.trim().length > 0) {
    formData.append("password", password.trim());
  }
  const res = await fetch(`${API_BASE}/api/scan-statement`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    try {
      const errJson = await res.json();
      let errorMsg = "Failed to scan statement.";
      let errorType = "STATEMENT_ERROR";
      if (errJson.detail) {
        if (typeof errJson.detail === "object") {
          errorMsg = errJson.detail.message || JSON.stringify(errJson.detail);
          errorType = errJson.detail.error_type || "STATEMENT_ERROR";
        } else {
          errorMsg = errJson.detail;
          if (errorMsg.toLowerCase().includes("password-protected") || errorMsg.toLowerCase().includes("password required")) {
            errorType = "PASSWORD_REQUIRED";
          } else if (errorMsg.toLowerCase().includes("incorrect") && errorMsg.toLowerCase().includes("password")) {
            errorType = "PASSWORD_INCORRECT";
          }
        }
      }
      const customErr: any = new Error(errorMsg);
      customErr.errorType = errorType;
      throw customErr;
    } catch (e: any) {
      if (e.errorType) throw e;
      if (e.message && e.message !== "Failed to scan statement.") {
        throw e;
      }
      const errorText = await res.text();
      throw new Error(errorText || "Failed to scan statement.");
    }
  }
  return await res.json();
}

/** Client-side fallback calculation if API is offline */
function fallbackEvaluate(req: TransactionCheckRequest): TransactionCheckResponse {
  const ratio = req.amount / Math.max(req.user_avg_amount, 5.0);
  let score = 0.05;
  const factors: RiskFactor[] = [];
  const safe: string[] = [];

  if (ratio >= 5.0) {
    score += 0.35;
    factors.push({
      type: "critical",
      title: "Unusual Transaction Volume",
      detail: `Amount (₹${req.amount.toFixed(2)}) is ${ratio.toFixed(1)}x higher than cardholder's usual average (₹${req.user_avg_amount.toFixed(2)}).`,
    });
  } else {
    safe.push("Purchase volume aligns with typical cardholder activity.");
  }

  if (req.is_foreign) {
    score += 0.28;
    factors.push({
      type: "warning",
      title: "Foreign / Cross-Border Origin",
      detail: "Transaction initiated outside your domestic country or from a foreign proxy IP.",
    });
  } else {
    safe.push("Transaction initiated within your domestic region.");
  }

  if (req.is_night_time) {
    score += 0.15;
    factors.push({
      type: "warning",
      title: "Unusual Night-Time Authorization",
      detail: "Requested during off-peak hours (1:00 AM – 5:00 AM).",
    });
  }

  if (!req.device_trusted) {
    score += 0.18;
    factors.push({
      type: "critical",
      title: "Unrecognized Device Fingerprint",
      detail: "No prior verified authorization record for this browser/device.",
    });
  } else {
    safe.push("Verified trusted device credentials.");
  }

  if (req.merchant_category === "crypto" || req.merchant_category === "jewelry") {
    score += 0.2;
    factors.push({
      type: "warning",
      title: "Elevated-Risk Merchant Sector",
      detail: `Merchant operates in ${req.merchant_category.toUpperCase()}, a sector subject to high unauthorized disputes.`,
    });
  }

  score = Math.min(Math.max(score, 0.02), 0.96);

  const status: "APPROVED" | "CHALLENGE" | "BLOCKED" =
    score >= 0.7 ? "BLOCKED" : score >= 0.3 ? "CHALLENGE" : "APPROVED";

  return {
    transaction_details: {
      amount: req.amount,
      merchant_name: req.merchant_name,
      category: req.merchant_category,
      channel: req.channel,
    },
    security_assessment: {
      fraud_probability: score,
      risk_score_percent: Math.round(score * 100),
      status,
      risk_tier: status === "BLOCKED" ? "High Risk" : status === "CHALLENGE" ? "Suspicious" : "Safe",
      theme: status === "BLOCKED" ? "danger" : status === "CHALLENGE" ? "warning" : "success",
      headline:
        status === "BLOCKED"
          ? "Transaction Blocked"
          : status === "CHALLENGE"
          ? "Verification Required"
          : "Transaction Approved",
      latency_ms: 1.2,
    },
    explanation: {
      risk_factors: factors,
      safety_factors: safe,
      recommended_action: {
        title: status === "BLOCKED" ? "Card Guarded" : status === "CHALLENGE" ? "SMS Passcode Sent" : "Cleared Instantly",
        summary:
          status === "BLOCKED"
            ? "This transaction has been blocked to protect your funds."
            : status === "CHALLENGE"
            ? "Suspicious indicators detected. A 6-digit confirmation code is required."
            : "Transaction verified safe and approved instantly.",
        steps:
          status === "BLOCKED"
            ? [
                "If this was not you, freeze your card immediately in mobile banking.",
                "If legitimate, confirm your identity to authorize.",
              ]
            : status === "CHALLENGE"
            ? ["Enter the 6-digit OTP code sent to your registered phone."]
            : ["Payment processed successfully."],
      },
    },
  };
}

