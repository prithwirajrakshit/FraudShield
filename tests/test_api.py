import io
import os
import unittest
import openpyxl
import torch
import asyncio
from fastapi import HTTPException, UploadFile

from backend.main import (
    health_check,
    get_sample_scenarios,
    check_transaction,
    scan_statement,
    scanner,
    predictor,
    mapper,
    TransactionCheckRequest
)
from src.data_pipeline import find_dataset_path
from src.focal_loss import BinaryFocalLoss

class TestFraudShield(unittest.TestCase):
    def test_01_health(self):
        res = health_check()
        self.assertEqual(res["status"], "healthy")
        self.assertEqual(res["engine"], "PyTorch Focal Loss Deep Network")

    def test_02_scenarios(self):
        scenarios = get_sample_scenarios()
        self.assertIsInstance(scenarios, list)
        self.assertGreaterEqual(len(scenarios), 4)
        for sc in scenarios:
            self.assertIn("id", sc)
            self.assertIn("data", sc)

    def test_03_check_transaction_safe(self):
        req = TransactionCheckRequest(
            amount=15.0,
            merchant_name="Corner Bakery",
            merchant_category="dining",
            channel="contactless",
            is_foreign=False,
            is_night_time=False,
            device_trusted=True,
            user_avg_amount=40.0,
            velocity_1h=1
        )
        res = check_transaction(req)
        self.assertEqual(res["security_assessment"]["status"], "APPROVED")
        self.assertEqual(res["security_assessment"]["risk_tier"], "Safe")
        self.assertIn("risk_factors", res["explanation"])

    def test_04_check_transaction_high_risk(self):
        req = TransactionCheckRequest(
            amount=4500.0,
            merchant_name="Overseas Crypto Vault",
            merchant_category="crypto",
            channel="online",
            is_foreign=True,
            is_night_time=True,
            device_trusted=False,
            user_avg_amount=50.0,
            velocity_1h=5
        )
        res = check_transaction(req)
        self.assertIn(res["security_assessment"]["status"], ("CHALLENGE", "BLOCKED"))
        self.assertGreater(len(res["explanation"]["risk_factors"]), 0)

    def test_05_scan_csv_statement(self):
        csv_bytes = (
            b"date,description,amount,channel\n"
            b"2026-10-28,Local Cafe,4.50,contactless\n"
            b"2026-10-29,Supermarket,65.20,in_store_chip\n"
        )
        res = scanner.scan_file(csv_bytes, "statement.csv")
        self.assertEqual(res["summary"]["total_transactions"], 2)
        self.assertEqual(len(res["transactions"]), 2)
        self.assertEqual(res["summary"]["account_health"], "Healthy")

    def test_06_scan_unencrypted_xlsx_statement(self):
        """Verifies Finding 1: .xlsx files must parse cleanly and not be confused with raw ZIPs."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Date", "Particulars", "Debit Amount"])
        ws.append(["2026-10-28", "Electronics Depot", "350.00"])
        ws.append(["2026-10-29", "Subway Restaurant", "12.50"])

        buf = io.BytesIO()
        wb.save(buf)
        xlsx_bytes = buf.getvalue()

        res = scanner.scan_file(xlsx_bytes, "bank_statement.xlsx")
        self.assertEqual(res["summary"]["total_transactions"], 2)
        self.assertEqual(res["transactions"][0]["description"], "Electronics Depot")
        self.assertEqual(res["transactions"][0]["amount"], 350.0)

    def test_07_scan_statement_size_limit(self):
        """Verifies Finding 3: Rejects uploads larger than 25 MB with HTTP 413."""
        huge_file = io.BytesIO(b"X" * (26 * 1024 * 1024))
        upload = UploadFile(filename="huge.csv", file=huge_file)
        with self.assertRaises(HTTPException) as ctx:
            scan_statement(file=upload)
        self.assertEqual(ctx.exception.status_code, 413)

    def test_08_find_dataset_path(self):
        """Verifies Finding 4: Locates creditcard.csv in benchmarks/ulb_credit_card/."""
        path = find_dataset_path()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith("creditcard.csv"))

    def test_09_binary_focal_loss_class_weighting(self):
        """Verifies Finding 16: Binary Focal Loss applies minority class alpha weighting."""
        loss_fn = BinaryFocalLoss(alpha=0.25, gamma=2.0)
        logits = torch.tensor([[2.0], [-2.0]], dtype=torch.float32)
        targets = torch.tensor([[1.0], [0.0]], dtype=torch.float32)
        loss = loss_fn(logits, targets)
        self.assertTrue(torch.is_tensor(loss))
        self.assertGreater(loss.item(), 0.0)

    def test_10_predictor_batch_inference(self):
        """Verifies Finding 11: predict_batch evaluates multi-row batches in a single pass."""
        scaled_row = mapper.map_to_features(amount=100.0)
        batch = torch.tensor(scaled_row).repeat(5, 1).numpy()
        preds = predictor.predict_batch(batch)
        self.assertEqual(len(preds), 5)
        for p in preds:
            self.assertIn("risk_score_percent", p)
            self.assertIn("status", p)

if __name__ == "__main__":
    unittest.main()
