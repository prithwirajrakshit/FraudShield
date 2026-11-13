import { Platform } from "react-native";

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

// Default backend URL: read from environment or platform default
let currentApiBase = process.env.EXPO_PUBLIC_API_URL || (Platform.OS === "android" ? "http://10.0.2.2:8000" : "http://localhost:8000");

export function getApiBase(): string {
  return currentApiBase;
}

export function setApiBase(url: string) {
  let cleaned = url.trim();
  if (cleaned.endsWith("/")) {
    cleaned = cleaned.slice(0, -1);
  }
  currentApiBase = cleaned;
}

export async function checkHealth(): Promise<{ status: string; engine?: string }> {
  try {
    const res = await fetch(`${currentApiBase}/api/health`, {
      method: "GET",
    });
    if (res.ok) {
      return await res.json();
    }
    return { status: "offline" };
  } catch (e) {
    return { status: "offline" };
  }
}

export async function checkTransaction(req: TransactionCheckRequest): Promise<TransactionCheckResponse> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 6000);
    const res = await fetch(`${currentApiBase}/api/check-transaction`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.warn("Backend server unavailable, running local evaluation engine:", err);
    return fallbackEvaluate(req);
  }
}

export async function getScenarios(): Promise<Scenario[]> {
  try {
    const res = await fetch(`${currentApiBase}/api/scenarios`);
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
        amount: 25.0,
        merchant_name: "Corner Bakery & Coffee",
        merchant_category: "dining",
        channel: "contactless",
        is_foreign: false,
        is_night_time: false,
        device_trusted: true,
        user_avg_amount: 100.0,
        velocity_1h: 1,
      },
    },
    {
      id: "groceries",
      name: "Supermarket Groceries",
      description: "₹86.20 domestic in-store card purchase",
      data: {
        amount: 450.0,
        merchant_name: "Whole Foods Market",
        merchant_category: "grocery",
        channel: "in_store_chip",
        is_foreign: false,
        is_night_time: false,
        device_trusted: true,
        user_avg_amount: 200.0,
        velocity_1h: 1,
      },
    },
    {
      id: "electronics_new_device",
      name: "High-Value Gadget on New Device",
      description: "₹890.00 online laptop order from a newly detected browser",
      data: {
        amount: 34999.0,
        merchant_name: "Apex Electronics Online",
        merchant_category: "electronics",
        channel: "online",
        is_foreign: false,
        is_night_time: false,
        device_trusted: false,
        user_avg_amount: 500.0,
        velocity_1h: 2,
      },
    },
    {
      id: "midnight_crypto",
      name: "Midnight Foreign Crypto Transfer",
      description: "₹2,450.00 transfer at 3:15 AM from an overseas IP gateway",
      data: {
        amount: 75000.0,
        merchant_name: "Global Crypto Vault Ltd",
        merchant_category: "crypto",
        channel: "online",
        is_foreign: true,
        is_night_time: true,
        device_trusted: false,
        user_avg_amount: 300.0,
        velocity_1h: 4,
      },
    },
  ];
}

export async function uploadStatement(
  file: { uri: string; name: string; mimeType?: string },
  password?: string
): Promise<StatementScanResponse> {
  const uploadUrl = `${currentApiBase}/api/scan-statement`;

  try {
    const formData = new FormData();

    // Read file binary bytes into a Uint8Array.
    // Expo WinterCG fetch (convertFormDataAsync) requires either a Blob or an object with a .bytes() method.
    // React Native's legacy { uri, name, type } dictionary throws "Unsupported FormDataPart implementation".
    let fileBytes: Uint8Array;
    try {
      const fetched = await fetch(file.uri);
      const buffer = await fetched.arrayBuffer();
      fileBytes = new Uint8Array(buffer);
    } catch (readErr) {
      const FileSystem = await import("expo-file-system/legacy");
      const b64 = await FileSystem.readAsStringAsync(file.uri, {
        encoding: FileSystem.EncodingType.Base64,
      });
      const binaryString = atob(b64);
      fileBytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        fileBytes[i] = binaryString.charCodeAt(i);
      }
    }

    const filePart = {
      name: file.name || "statement.pdf",
      type: file.mimeType || "application/pdf",
      bytes: async () => fileBytes,
    };

    formData.append("file", filePart as any);

    if (password && password.trim().length > 0) {
      formData.append("password", password.trim());
    }

    const res = await fetch(uploadUrl, {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
      body: formData,
    });

    if (!res.ok) {
      const errJson = await res.json().catch(() => null);
      let errorMsg = `Server returned ${res.status}`;
      let errorType = "STATEMENT_ERROR";
      if (errJson?.detail) {
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
    }

    return await res.json();
  } catch (err: any) {
    if (err.errorType) {
      throw err;
    }
    throw new Error(err.message || "Failed to scan bank statement. Please verify server connection.");
  }
}

export function fallbackEvaluate(req: TransactionCheckRequest): TransactionCheckResponse {
  let score = 0.04;
  const factors: RiskFactor[] = [];
  const safe: string[] = [];

  const ratio = req.amount / Math.max(req.user_avg_amount, 5);
  if (ratio >= 4.0) {
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
      title: "Cross-Border Foreign Gateway",
      detail: "Transaction initiated through an overseas payment routing gateway.",
    });
  } else {
    safe.push("Domestic origin verified.");
  }

  if (req.is_night_time) {
    score += 0.16;
    factors.push({
      type: "warning",
      title: "Off-Hours Authorization Request",
      detail: "Payment initiated during low-activity night hours (1:00 AM – 5:00 AM).",
    });
  }

  if (!req.device_trusted) {
    score += 0.18;
    factors.push({
      type: "critical",
      title: "Unrecognized Device Fingerprint",
      detail: "No prior verified authorization record for this terminal/device.",
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
          ? "Transaction Guarded (High Threat)"
          : status === "CHALLENGE"
          ? "Two-Factor Challenge Required"
          : "Verified Legitimate Purchase",
      latency_ms: 1.2,
    },
    explanation: {
      risk_factors: factors,
      safety_factors: safe,
      recommended_action: {
        title: status === "BLOCKED" ? "Card Temporarily Guarded" : status === "CHALLENGE" ? "SMS Passcode Sent" : "Cleared Instantly",
        summary:
          status === "BLOCKED"
            ? "This transaction has been blocked to protect your funds from unauthorized takeover."
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

