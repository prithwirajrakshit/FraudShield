import os
import sys
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# Ensure project root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.feature_mapper import FeatureMapper
from backend.services.predictor import FraudPredictor
from backend.services.explainer import TransactionExplainer
from backend.services.statement_scanner import StatementScanner, PasswordRequiredError, IncorrectPasswordError

app = FastAPI(
    title="FraudShield Real-Time Payment Security API",
    description="Consumer and Merchant Payment Fraud Detection Engine powered by Deep Focal Neural Network",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve model paths relative to repo root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
mapper = FeatureMapper(scaler_path=os.path.join(BASE_DIR, "models", "scaler.joblib"))
predictor = FraudPredictor(model_path=os.path.join(BASE_DIR, "models", "best_focal_dnn.pt"))
scanner = StatementScanner(mapper=mapper, predictor=predictor)

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB limit

class TransactionCheckRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction monetary value in currency units")
    merchant_name: Optional[str] = Field("General Merchant", description="Store or business name")
    merchant_category: str = Field("general", description="Merchant sector (grocery, dining, electronics, crypto, etc.)")
    channel: str = Field("online", description="Transaction method: in_store_chip, contactless, online, atm")
    is_foreign: bool = Field(False, description="Whether transaction originated outside domestic country")
    is_night_time: bool = Field(False, description="Whether transaction occurred between 1 AM and 5 AM")
    device_trusted: bool = Field(True, description="Whether transaction device/browser is already trusted")
    user_avg_amount: float = Field(50.0, gt=0, description="Cardholder's typical average transaction volume")
    velocity_1h: int = Field(1, ge=1, description="Number of transactions initiated in the last 60 minutes")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FraudShield API",
        "engine": "PyTorch Focal Loss Deep Network"
    }

@app.get("/api/scenarios")
def get_sample_scenarios():
    """Returns realistic preset scenarios for one-click testing in the frontend."""
    return [
        {
            "id": "coffee",
            "name": "Everyday Coffee Purchase",
            "description": "₹4.50 at a local cafe on your regular morning commute",
            "data": {
                "amount": 4.50,
                "merchant_name": "Corner Bakery & Coffee",
                "merchant_category": "dining",
                "channel": "contactless",
                "is_foreign": False,
                "is_night_time": False,
                "device_trusted": True,
                "user_avg_amount": 40.0,
                "velocity_1h": 1
            }
        },
        {
            "id": "groceries",
            "name": "Weekly Supermarket Run",
            "description": "₹86.20 domestic in-store chip purchase at supermarket",
            "data": {
                "amount": 86.20,
                "merchant_name": "Whole Foods Market",
                "merchant_category": "grocery",
                "channel": "in_store_chip",
                "is_foreign": False,
                "is_night_time": False,
                "device_trusted": True,
                "user_avg_amount": 50.0,
                "velocity_1h": 1
            }
        },
        {
            "id": "electronics_unrecognized",
            "name": "High-Value Gadget on New Device",
            "description": "₹890.00 online laptop purchase from an unrecognized device",
            "data": {
                "amount": 890.00,
                "merchant_name": "Apex Electronics Online",
                "merchant_category": "electronics",
                "channel": "online",
                "is_foreign": False,
                "is_night_time": False,
                "device_trusted": False,
                "user_avg_amount": 65.0,
                "velocity_1h": 2
            }
        },
        {
            "id": "midnight_crypto_attack",
            "name": "Midnight Overseas Crypto Drain",
            "description": "₹2,450.00 transfer at 3:15 AM from a foreign IP address",
            "data": {
                "amount": 2450.00,
                "merchant_name": "Global Crypto Vault Ltd",
                "merchant_category": "crypto",
                "channel": "online",
                "is_foreign": True,
                "is_night_time": True,
                "device_trusted": False,
                "user_avg_amount": 45.0,
                "velocity_1h": 4
            }
        }
    ]

@app.post("/api/check-transaction")
def check_transaction(req: TransactionCheckRequest):
    try:
        scaled_features = mapper.map_to_features(
            amount=req.amount,
            merchant_category=req.merchant_category,
            channel=req.channel,
            is_foreign=req.is_foreign,
            is_night_time=req.is_night_time,
            device_trusted=req.device_trusted,
            user_avg_amount=req.user_avg_amount,
            velocity_1h=req.velocity_1h
        )

        prediction = predictor.predict(scaled_features)
        explanation = TransactionExplainer.generate_explanation(
            amount=req.amount,
            merchant_category=req.merchant_category,
            channel=req.channel,
            is_foreign=req.is_foreign,
            is_night_time=req.is_night_time,
            device_trusted=req.device_trusted,
            user_avg_amount=req.user_avg_amount,
            velocity_1h=req.velocity_1h,
            prediction_result=prediction
        )

        return {
            "transaction_details": {
                "amount": req.amount,
                "merchant_name": req.merchant_name,
                "category": req.merchant_category,
                "channel": req.channel
            },
            "security_assessment": prediction,
            "explanation": explanation
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scan-statement")
def scan_statement(
    file: UploadFile = File(...),
    password: Optional[str] = Form(None)
):
    try:
        content = file.file.read(MAX_FILE_SIZE + 1)
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail={
                    "error_type": "STATEMENT_ERROR",
                    "message": "File exceeds maximum permitted size of 25 MB.",
                    "title": "Payload Too Large"
                }
            )
        scan_report = scanner.scan_file(content, filename=file.filename or "statement.csv", password=password)
        return scan_report
    except PasswordRequiredError as pe:
        raise HTTPException(
            status_code=400,
            detail={
                "error_type": "PASSWORD_REQUIRED",
                "message": str(pe),
                "title": "Password Protected Statement"
            }
        )
    except IncorrectPasswordError as ipe:
        raise HTTPException(
            status_code=400,
            detail={
                "error_type": "PASSWORD_INCORRECT",
                "message": str(ipe),
                "title": "Incorrect Statement Password"
            }
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail={
                "error_type": "STATEMENT_ERROR",
                "message": str(ve),
                "title": "Statement Processing Error"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error_type": "SERVER_ERROR",
                "message": str(e),
                "title": "Server Error"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

