from typing import List, Dict, Any

class TransactionExplainer:
    """
    Translates raw and behavioral transaction attributes into clear,
    plain-English reasons suitable for consumers and business clients.
    """
    @staticmethod
    def generate_explanation(
        amount: float,
        merchant_category: str,
        channel: str,
        is_foreign: bool,
        is_night_time: bool,
        device_trusted: bool,
        user_avg_amount: float,
        velocity_1h: int,
        prediction_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        status = prediction_result["status"]
        reasons: List[Dict[str, str]] = []
        positive_factors: List[str] = []
        
        ratio = amount / max(user_avg_amount, 5.0)

        # 1. Amount Evaluation
        if ratio >= 5.0:
            reasons.append({
                "type": "critical",
                "title": "Unusual Transaction Volume",
                "detail": f"Amount (₹{amount:,.2f}) is {ratio:.1f}x higher than the typical spending average (₹{user_avg_amount:,.2f})."
            })
        elif ratio >= 2.5:
            reasons.append({
                "type": "warning",
                "title": "Elevated Amount",
                "detail": f"Purchase is noticeably higher than your standard purchases (₹{user_avg_amount:,.2f})."
            })
        else:
            positive_factors.append("Transaction amount is consistent with historical cardholder spending patterns.")

        # 2. Location & Cross-Border
        if is_foreign:
            reasons.append({
                "type": "warning",
                "title": "Foreign / Cross-Border Origin",
                "detail": "Initiated outside domestic borders or from an overseas IP gateway."
            })
        else:
            positive_factors.append("Purchase initiated within your primary registered geographical region.")

        # 3. Temporal Anomaly
        if is_night_time:
            reasons.append({
                "type": "warning",
                "title": "Unusual Authorization Timing",
                "detail": "Payment requested during off-peak night hours (1:00 AM – 5:00 AM local time)."
            })

        # 4. Device Trust
        if not device_trusted:
            reasons.append({
                "type": "critical",
                "title": "Unrecognized Terminal or Device",
                "detail": "Device fingerprint has no prior verified login or authorization record on this account."
            })
        else:
            positive_factors.append("Verified trusted browser/device fingerprint.")

        # 5. Merchant Category Risk
        high_risk_cats = {
            "crypto": "Cryptocurrency / Digital Asset Exchange",
            "wire_transfer": "High-Volume Wire Transfer",
            "jewelry": "Luxury Jewelry & Precious Metals",
            "gaming": "Online Casino / Gambling Platform"
        }
        if merchant_category.lower() in high_risk_cats:
            reasons.append({
                "type": "warning",
                "title": "High-Risk Merchant Sector",
                "detail": f"Merchant operates in {high_risk_cats[merchant_category.lower()]}, a sector with elevated dispute and fraud frequencies."
            })

        # 6. Velocity / Frequency
        if velocity_1h >= 3:
            reasons.append({
                "type": "warning",
                "title": "Rapid Transaction Frequency",
                "detail": f"{velocity_1h} transactions attempted within the last 60 minutes."
            })

        # Recommended Action Guidance
        if status == "BLOCKED":
            action = {
                "title": "Card Temporarily Guarded",
                "summary": "This charge has been blocked to protect your funds from unauthorized takeover.",
                "steps": [
                    "If you did not authorize this payment, freeze your card instantly in your mobile banking app.",
                    "If this was a legitimate purchase, tap 'Confirm Identity' below to unblock merchant."
                ]
            }
        elif status == "CHALLENGE":
            action = {
                "title": "One-Time Security Verification",
                "summary": "Suspicious indicators detected. A 6-digit confirmation passcode is required.",
                "steps": [
                    "A secure authorization code has been sent via SMS to your registered phone number.",
                    "Enter the code to approve this single purchase."
                ]
            }
        else:
            action = {
                "title": "Cleared Instantly",
                "summary": "Transaction verified safe against all fraud screening benchmarks.",
                "steps": [
                    "Cleared through instant authorization pipeline.",
                    "Receipt and digital confirmation delivered to your account."
                ]
            }

        return {
            "risk_factors": reasons,
            "safety_factors": positive_factors,
            "recommended_action": action
        }

