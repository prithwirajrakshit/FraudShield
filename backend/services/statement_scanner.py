import io
import re
import zipfile
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple

import pyzipper
import msoffcrypto
from pypdf import PdfReader
import pdfplumber

from backend.services.feature_mapper import FeatureMapper
from backend.services.predictor import FraudPredictor
from backend.services.explainer import TransactionExplainer

class PasswordRequiredError(ValueError):
    """Raised when a bank statement is encrypted and no password or an empty password was supplied."""
    pass

class IncorrectPasswordError(ValueError):
    """Raised when an encrypted bank statement fails decryption with the supplied password."""
    pass

class StatementScanner:
    """
    Universal Adaptive Bank Statement Scanner & Fraud Analyzer.
    
    Dynamically normalizes and analyzes statements from ANY bank (State Bank of India,
    HDFC, ICICI, Axis, Kotak Mahindra, PNB, Bank of Baroda, Canara, Union Bank,
    IndusInd, Federal, Chase, Barclays, Revolut, etc.) without requiring pre-configured
    bank-specific templates.
    """

    # Comprehensive aliases for fuzzy column mapping across global & Indian banks
    DATE_ALIASES = [
        "transaction_date", "txn_date", "tran_date", "posting_date", "post_date",
        "value_date", "val_date", "value_dt", "date", "trans_date", "booking_date",
        "activity_date", "date_of_transaction", "payment_date"
    ]

    DESC_ALIASES = [
        "narration", "description", "particulars", "transaction_details", "details",
        "remarks", "transaction_remarks", "payee", "merchant", "payee_name",
        "memo", "reference_narration", "payment_details", "name", "title"
    ]

    DEBIT_ALIASES = [
        "withdrawal_amount", "withdrawal_amt", "debit_amount", "debit_amt",
        "withdrawal", "debit", "withdrawals", "debits", "paid_out", "spent",
        "charge", "dr_amount", "debit_dr", "withdrawal_dr", "dr"
    ]

    CREDIT_ALIASES = [
        "deposit_amount", "deposit_amt", "credit_amount", "credit_amt",
        "deposit", "credit", "deposits", "credits", "paid_in", "received",
        "cr_amount", "credit_cr", "deposit_cr", "cr"
    ]

    AMOUNT_ALIASES = [
        "amount", "txn_amount", "transaction_amount", "amt", "net_amount",
        "total_amount"
    ]

    TYPE_ALIASES = [
        "dr_cr", "cr_dr", "dr_or_cr", "cr_or_dr", "type", "txn_type",
        "transaction_type", "d_c", "indicator", "cr_dr_flag"
    ]

    BALANCE_ALIASES = [
        "balance", "closing_balance", "closing_bal", "running_balance",
        "available_balance", "net_balance", "bal", "balance_inr"
    ]

    REF_ALIASES = [
        "chq_ref_no", "ref_no_cheque_no", "ref_no", "cheque_no", "chq_no",
        "cheque_number", "utr", "txn_id", "reference_number", "cheque", "ref"
    ]

    # Precise word-boundary anchored patterns to eliminate summary/metadata rows
    NOISE_PATTERNS = [
        r"\bstatement\s*summary\b",
        r"\bopening\s*balance\b",
        r"\bclosing\s*balance\b",
        r"\bbrought\s*forward\b",
        r"\bcarried\s*forward\b",
        r"\bb/f\b",
        r"\bc/f\b",
        r"\btotal\s*debits?\b",
        r"\btotal\s*credits?\b",
        r"\btotal\s*withdrawals?\b",
        r"\btotal\s*deposits?\b",
        r"\bdr\s*count\b",
        r"\bcr\s*count\b",
        r"\bend\s*of\s*statement\b",
        r"\bgenerated\s*on\b",
        r"\bpage\s*\d+\s*of\s*\d+\b",
        r"\bcomputer\s*generated\b",
        r"\bdo\s*not\s*share\b",
        r"\bregistered\s*office\b",
        r"\bpower\s*of\s*attorney\b",
        r"\bdisclaimer\b",
        r"\bimportant\s*information\b"
    ]

    # Calendar date format patterns for validation
    DATE_PATTERNS = [
        r"^\d{1,4}[/\-\.]\d{1,2}[/\-\.]\d{1,4}$",
        r"^\d{1,2}[\s\-][A-Za-z]{3,9}[\s\-]\d{2,4}$",
        r"^[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4}$",
        r"^\d{1,4}[/\-\.]\d{1,2}[/\-\.]\d{1,4}\s+\d{1,2}:\d{2}(:\d{2})?$"
    ]

    def __init__(self, mapper: FeatureMapper, predictor: FraudPredictor):
        self.mapper = mapper
        self.predictor = predictor

    @staticmethod
    def clean_text(val: Any) -> str:
        """Strips whitespace, control chars, and multi-line breaks into a clean string."""
        if pd.isna(val):
            return ""
        s = str(val).strip()
        if s.lower() in ("nan", "none", "null", "-", "nil"):
            return ""
        return " ".join(s.split())

    @staticmethod
    def clean_amount(val: Any) -> float:
        """
        Parses monetary strings into a clean positive float:
        Supports ₹, $, €, £, comma grouping, decimal notation, and signed numbers.
        """
        if pd.isna(val):
            return 0.0
        if isinstance(val, (int, float)):
            return float(abs(val))
        val_str = str(val).strip()
        if not val_str or val_str.lower() in ("nan", "none", "-", "nil", ""):
            return 0.0
        cleaned = re.sub(r"[^\d.,\-+]", "", val_str)
        if not cleaned:
            return 0.0
        if "," in cleaned and "." in cleaned:
            if cleaned.rfind(",") > cleaned.rfind("."):
                cleaned = cleaned.replace(".", "").replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")
        elif "," in cleaned and "." not in cleaned:
            cleaned = cleaned.replace(",", ".")
        try:
            return float(abs(float(cleaned)))
        except ValueError:
            return 0.0

    @classmethod
    def is_valid_date(cls, val: str) -> bool:
        """Validates if a text token actually represents a calendar date."""
        v = val.strip()
        if not v:
            return False
        return any(re.match(p, v, re.IGNORECASE) for p in cls.DATE_PATTERNS)

    @classmethod
    def is_noise_row(cls, row_values: List[str]) -> bool:
        """Determines if a row is a bank summary/metadata/footer row rather than a transaction."""
        row_text = " ".join(row_values).lower()
        if not row_text.strip():
            return True
        for pattern in cls.NOISE_PATTERNS:
            if re.search(pattern, row_text):
                return True
        return False

    @staticmethod
    def normalize_col_name(col: Any) -> str:
        """Normalizes raw header strings: 'Withdrawal Amt. (INR )' -> 'withdrawal_amt_inr'."""
        s = str(col).strip().lower()
        s = re.sub(r"[^\w\s]", " ", s)
        s = re.sub(r"\s+", "_", s).strip("_")
        return s

    @classmethod
    def find_best_header_row(cls, df_raw: pd.DataFrame, max_rows: int = 50) -> Tuple[int, int]:
        """
        Intelligently identifies the table header row by scoring rows against bank header keywords.
        Returns (best_row_index, best_score).
        """
        header_keywords = {
            "date", "txn_date", "tran_date", "value_date", "posting_date",
            "particulars", "narration", "description", "details", "remarks",
            "debit", "withdrawal", "dr", "paid_out",
            "credit", "deposit", "cr", "paid_in",
            "amount", "amt", "balance", "bal", "chq", "cheque", "ref"
        }

        best_row = 0
        best_score = -1

        for r in range(min(max_rows, len(df_raw))):
            raw_cells = [
                str(cell).strip()
                for cell in df_raw.iloc[r]
                if pd.notna(cell) and str(cell).strip()
            ]
            if not raw_cells:
                continue

            # 1. Reject data rows that contain actual transaction dates (e.g. 02/10/2026)
            if any(cls.is_valid_date(c) for c in raw_cells):
                continue

            # 2. Reject statement summary / footer rows (e.g. Brought Forward, Dr Count, Total Debits)
            row_summary_text = " ".join(raw_cells).lower()
            if any(k in row_summary_text for k in ["brought forward", "dr count", "cr count", "total debits", "total credits", "closing balance", "statement summary"]):
                continue

            row_cells = [cls.normalize_col_name(cell) for cell in raw_cells]

            score = 0
            has_date = False
            has_desc = False
            has_amount = False

            for cell in row_cells:
                matched_kw = [kw for kw in header_keywords if kw in cell]
                if matched_kw:
                    score += len(matched_kw)
                if any(k in cell for k in ["date", "txn_date", "tran_date", "value_date"]):
                    has_date = True
                if any(k in cell for k in ["particulars", "narration", "description", "details", "remarks", "payee", "merchant"]):
                    has_desc = True
                if any(k in cell for k in ["debit", "credit", "withdrawal", "deposit", "amount", "balance", "dr", "cr"]):
                    has_amount = True

            if has_date and (has_desc or has_amount):
                score += 5
            if has_date and has_desc and has_amount:
                score += 10

            if score > best_score:
                best_score = score
                best_row = r

        return best_row, best_score

    @classmethod
    def map_columns(cls, columns: List[str]) -> Dict[str, Optional[str]]:
        """
        Fuzzy-maps table columns into canonical roles:
        date_col, desc_col, debit_col, credit_col, amt_col, type_col, balance_col, ref_col.
        """
        norm_map = {col: cls.normalize_col_name(col) for col in columns}

        # 1. Type column (DR / CR indicator) - detect FIRST so it is not captured as debit/credit
        type_col = None
        for orig, norm in norm_map.items():
            if norm in cls.TYPE_ALIASES or ("dr" in norm and "cr" in norm):
                type_col = orig
                break

        # 2. Balance column - detect so it is never confused with amount or debit
        balance_col = None
        for orig, norm in norm_map.items():
            if any(bal in norm for bal in cls.BALANCE_ALIASES) and orig != type_col:
                balance_col = orig
                break

        eligible = {
            orig: norm for orig, norm in norm_map.items()
            if orig != balance_col and orig != type_col
        }

        # 3. Date column
        date_col = None
        for alias in cls.DATE_ALIASES:
            for orig, norm in norm_map.items():
                if norm == alias or (alias in norm and "date" in norm):
                    date_col = orig
                    break
            if date_col:
                break
        if not date_col:
            for orig, norm in norm_map.items():
                if "date" in norm or "val_dt" in norm or norm.endswith("_dt"):
                    date_col = orig
                    break

        # 4. Description / Narration column
        desc_col = None
        for alias in cls.DESC_ALIASES:
            for orig, norm in norm_map.items():
                if norm == alias or alias in norm:
                    desc_col = orig
                    break
            if desc_col:
                break

        # 5. Debit / Withdrawal column
        debit_col = None
        for alias in cls.DEBIT_ALIASES:
            for orig, norm in eligible.items():
                if norm == alias or (alias in norm and not any(cr in norm for cr in ["credit", "cr_amount"])):
                    debit_col = orig
                    break
            if debit_col:
                break

        # 6. Credit / Deposit column
        credit_col = None
        for alias in cls.CREDIT_ALIASES:
            for orig, norm in eligible.items():
                if norm == alias or (alias in norm and not any(dr in norm for dr in ["debit", "withdrawal"])):
                    credit_col = orig
                    break
            if credit_col:
                break

        # 7. Generic Amount column
        amt_col = None
        for alias in cls.AMOUNT_ALIASES:
            for orig, norm in eligible.items():
                if norm == alias or alias in norm:
                    if orig != debit_col and orig != credit_col:
                        amt_col = orig
                        break
            if amt_col:
                break

        # 8. Cheque / Reference number column
        ref_col = None
        for alias in cls.REF_ALIASES:
            for orig, norm in norm_map.items():
                if norm == alias or alias in norm:
                    ref_col = orig
                    break
            if ref_col:
                break

        return {
            "date_col": date_col,
            "desc_col": desc_col,
            "debit_col": debit_col,
            "credit_col": credit_col,
            "amt_col": amt_col,
            "type_col": type_col,
            "balance_col": balance_col,
            "ref_col": ref_col
        }

    @staticmethod
    def infer_category(desc: str) -> str:
        """
        Infers transaction category from merchant narrative with comprehensive
        Indian and international merchant entity recognition.
        """
        d = desc.lower()

        # Crypto & Digital Assets
        if any(k in d for k in ["crypto", "binance", "coinbase", "kraken", "btc", "eth", "wazirx", "kucoin", "coindcx", "coinswitch"]):
            return "crypto"

        # Food, Dining & Quick Deliveries
        if any(k in d for k in ["cafe", "coffee", "starbucks", "subway", "restaurant", "burger", "pizza", "zomato", "swiggy", "food", "bakery", "bar", "mcdonald", "kfc", "domino", "haldiram"]):
            return "dining"

        # Groceries & Daily Needs
        if any(k in d for k in ["grocery", "supermarket", "walmart", "trader", "whole foods", "mart", "aldi", "costco", "tesco", "kroger", "zepto", "blinkit", "bigbasket", "instamart", "dmart", "spencer", "reliance fresh", "kirana"]):
            return "grocery"

        # Transport, Fuel & Travel
        if any(k in d for k in ["uber", "lyft", "shell", "chevron", "petrol", "gas", "fuel", "transit", "train", "metro", "airline", "flight", "ola", "rapido", "irctc", "indigo", "air india", "hpcl", "bpcl", "iocl"]):
            return "transport"

        # Electronics & Hardware
        if any(k in d for k in ["apple", "electronics", "best buy", "tech", "laptop", "mobile", "gadget", "samsung", "croma", "reliance digital", "vijay sales"]):
            return "electronics"

        # Luxury & Jewelry
        if any(k in d for k in ["jewelry", "gold", "diamond", "luxury", "rolex", "gucci", "prada", "tanishq", "malabar", "kalyan"]):
            return "jewelry"

        # Travel & Hotels
        if any(k in d for k in ["hotel", "marriott", "airbnb", "booking", "expedia", "resort", "travel", "makemytrip", "agoda", "yatra", "cleartrip"]):
            return "travel"

        # Gaming & Casinos
        if any(k in d for k in ["casino", "gaming", "steam", "dream11", "rummy", "poker", "playstation", "xbox", "bet"]):
            return "gaming"

        # ATM Cash Withdrawals
        if any(k in d for k in ["atm", "cash withdrawal", "dispense", "atm-midnight", "cash wdl", "self wdl"]):
            return "atm"

        # Utilities & Bill Payments
        if any(k in d for k in ["airtel", "jio", "vodafone", "electricity", "billdesk", "bbps", "bescom", "tata power", "gas bill", "water bill"]):
            return "utilities"

        # Shopping & E-Commerce
        if any(k in d for k in ["amazon", "flipkart", "myntra", "ajio", "zara", "nykaa", "shopping"]):
            return "clothing"

        # Inter-bank transfers & UPI
        if any(k in d for k in ["upi", "neft", "imps", "rtgs", "transfer", "tfr"]):
            return "wire_transfer"

        return "general"

    def extract_file_content(self, file_bytes: bytes, filename: str, password: Optional[str] = None) -> pd.DataFrame:
        """
        Unlocks (if password-protected) and parses statement files into a pandas DataFrame.
        Supports ZIP (AES/Standard), XLSX/XLS (msoffcrypto), PDF (pypdf), and CSV/TSV.
        """
        lower_name = filename.lower()
        pwd_bytes = password.encode("utf-8") if password else None

        # 1. Excel Statements (.xlsx / .xls) - Checked first because .xlsx files have ZIP (PK..) signatures
        if lower_name.endswith(".xlsx") or lower_name.endswith(".xls"):
            file_stream = io.BytesIO(file_bytes)
            try:
                office_file = msoffcrypto.OfficeFile(file_stream)
                if office_file.is_encrypted():
                    if not password or not password.strip():
                        raise PasswordRequiredError("This Excel bank statement is password-protected. Please enter your password to unlock.")
                    decrypted_stream = io.BytesIO()
                    try:
                        office_file.load_key(password=password.strip())
                        office_file.decrypt(decrypted_stream)
                        raw_stream = decrypted_stream
                    except (msoffcrypto.exceptions.InvalidPasswordError, msoffcrypto.exceptions.DecryptionError):
                        raise IncorrectPasswordError("Incorrect Excel statement password. Please verify your bank's password format (e.g. DOB or Mobile Number) and try again.")
                else:
                    file_stream.seek(0)
                    raw_stream = file_stream

                raw_stream.seek(0)
                df_excel = pd.read_excel(raw_stream, header=None, dtype=str)
                return df_excel
            except (PasswordRequiredError, IncorrectPasswordError):
                raise
            except Exception as e:
                err_str = str(e).lower()
                if "password" in err_str or "encrypted" in err_str:
                    if not password or not password.strip():
                        raise PasswordRequiredError("This Excel bank statement is password-protected. Please enter your password to unlock.")
                    else:
                        raise IncorrectPasswordError("Incorrect Excel statement password. Please verify and re-enter your password.")
                raise ValueError(f"Unable to read Excel statement: {str(e)}")

        # 2. Password-Protected ZIP archive
        if lower_name.endswith(".zip") or file_bytes[:4] == b"PK\x03\x04":
            try:
                with pyzipper.AESZipFile(io.BytesIO(file_bytes)) as z:
                    if pwd_bytes:
                        z.setpassword(pwd_bytes)
                    target_file = None
                    for item in z.infolist():
                        if any(item.filename.lower().endswith(ext) for ext in [".xlsx", ".xls", ".csv", ".txt"]):
                            target_file = item.filename
                            break
                    if not target_file:
                        target_file = z.namelist()[0]
                    extracted_data = z.read(target_file, pwd=pwd_bytes)
                    return self.extract_file_content(extracted_data, target_file, password)
            except RuntimeError as e:
                if "password" in str(e).lower() or "bad password" in str(e).lower() or "encrypted" in str(e).lower():
                    if not password or not password.strip():
                        raise PasswordRequiredError("This ZIP bank statement is password-protected. Please enter your password to unlock.")
                    else:
                        raise IncorrectPasswordError("Incorrect ZIP statement password. Please verify and re-enter your password.")
                raise ValueError(f"Failed to unlock ZIP archive: {str(e)}")
            except Exception as e:
                raise ValueError(f"Unable to read ZIP archive: {str(e)}")

        # 3. PDF Statements (.pdf)
        if lower_name.endswith(".pdf") or file_bytes[:4] == b"%PDF":
            # Step A: Validate and enforce password protection
            clean_pwd = password.strip() if password and password.strip() else None
            try:
                reader = PdfReader(io.BytesIO(file_bytes))
                if reader.is_encrypted:
                    if not clean_pwd:
                        raise PasswordRequiredError("This PDF bank statement is password-protected. Please enter your statement password to unlock.")
                    try:
                        status = reader.decrypt(clean_pwd)
                        if status == 0:
                            raise IncorrectPasswordError("Incorrect PDF statement password. Please verify and re-enter your password.")
                    except (PasswordRequiredError, IncorrectPasswordError):
                        raise
                    except Exception:
                        raise IncorrectPasswordError("Incorrect PDF statement password. Please verify and re-enter your password.")
            except (PasswordRequiredError, IncorrectPasswordError):
                raise
            except Exception:
                pass

            # Step B: Advanced Multi-Stage PDF Table and Layout Extraction
            structured_rows = []

            # Stage 1: Try pdfplumber table and text extraction in a single open pass
            try:
                with pdfplumber.open(io.BytesIO(file_bytes), password=clean_pwd) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        if tables:
                            for tbl in tables:
                                for row in tbl:
                                    if row and any(c is not None and str(c).strip() for c in row):
                                        clean_r = [str(c).strip() if c is not None else "" for c in row]
                                        if sum(1 for c in clean_r if c) >= 2:
                                            structured_rows.append(clean_r)
                        else:
                            text_tables = page.extract_tables(table_settings={
                                "vertical_strategy": "text",
                                "horizontal_strategy": "text",
                                "snap_tolerance": 4,
                                "join_tolerance": 4
                            })
                            if text_tables:
                                for tbl in text_tables:
                                    for row in tbl:
                                        if row and any(c is not None and str(c).strip() for c in row):
                                            clean_r = [str(c).strip() if c is not None else "" for c in row]
                                            if sum(1 for c in clean_r if c) >= 2:
                                                structured_rows.append(clean_r)

                    # Stage 2: Fallback to Layout-Aware Text extraction within the same open handle
                    if not structured_rows or len(structured_rows) < 3:
                        pdf_lines = []
                        for page in pdf.pages:
                            txt = page.extract_text(layout=True)
                            if txt:
                                pdf_lines.extend(txt.splitlines())

                        for line in pdf_lines:
                            line_str = line.strip()
                            if not line_str:
                                continue
                            tokens = [t.strip() for t in re.split(r"\s{2,}|\t", line_str) if t.strip()]
                            if len(tokens) >= 3 or (len(tokens) == 2 and any(self.is_valid_date(tok) for tok in tokens)):
                                structured_rows.append(tokens)
                            else:
                                match = re.match(
                                    r"^(\d{1,4}[/\-\.]\d{1,2}[/\-\.]\d{1,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})\s+(.+?)\s+([0-9,]+\.\d{2}|[0-9,]+(?:\s*[Dd][Rr]|\s*[Cc][Rr])?)(?:\s+([0-9,]+\.\d{2}.*))?$",
                                    line_str
                                )
                                if match:
                                    dt = match.group(1).strip()
                                    desc = match.group(2).strip()
                                    amt1 = match.group(3).strip()
                                    amt2 = match.group(4).strip() if match.group(4) else ""
                                    structured_rows.append([dt, desc, amt1, amt2])
            except Exception:
                pass

            if not structured_rows:
                raise ValueError("No readable transaction text could be extracted from this PDF. Please check if it contains scanned images or an unsupported layout.")

            max_cols = max(len(r) for r in structured_rows)
            padded = [r + [""] * (max_cols - len(r)) for r in structured_rows]
            return pd.DataFrame(padded, dtype=str)

        # 4. Standard CSV / TSV / Text Files
        encodings_to_try = ["utf-8-sig", "utf-8", "latin-1", "cp1252"]
        raw_text = None
        for enc in encodings_to_try:
            try:
                raw_text = file_bytes.decode(enc)
                break
            except (UnicodeDecodeError, LookupError):
                continue

        if not raw_text:
            raw_text = file_bytes.decode("utf-8", errors="ignore")

        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        if not lines:
            raise ValueError("The statement file is empty or could not be decoded.")

        # Detect the real CSV header line by scanning keyword density
        keywords = {
            "date", "txn_date", "tran_date", "value_date", "particulars", "narration",
            "description", "details", "debit", "withdrawal", "credit", "deposit",
            "amount", "balance", "dr", "cr"
        }
        best_header_idx = 0
        best_score = -1
        for idx, line in enumerate(lines[:50]):
            line_clean = re.sub(r"[^\w\s,;|\t]", " ", line.lower())
            tokens = set(re.split(r"[,;|\t\s]+", line_clean))
            matches = keywords.intersection(tokens)
            score = len(matches) * 3
            delims = max(line.count(","), line.count(";"), line.count("\t"), line.count("|"))
            if delims >= 2:
                score += delims
            if score > best_score and len(matches) >= 2:
                best_score = score
                best_header_idx = idx

        csv_body = "\n".join(lines[best_header_idx:])
        # Auto-detect delimiter
        sample_line = lines[best_header_idx]
        sep = "\t" if "\t" in sample_line else (";" if ";" in sample_line else ",")
        df_csv = pd.read_csv(io.StringIO(csv_body), sep=sep, dtype=str)
        return df_csv

    def parse_statement_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Normalizes any bank's tabular data into a canonical list of debit transactions.
        Handles continuation lines, debit/credit splitting, and noise removal.
        """
        # 0. Drop noise rows (summary tables, header/footer notes) before column scoring
        noise_idx = []
        for i, r in df.iterrows():
            vals = [str(v).strip() for v in r.values]
            has_date = self.is_valid_date(vals[0]) or (len(vals) > 1 and self.is_valid_date(vals[1]))
            if self.is_noise_row(vals):
                noise_idx.append(i)
            elif not has_date and any(w in " ".join(vals).lower() for w in ["brought forward", "dr count", "cr count", "total debits", "total credits", "closing balance", "statement summary", "grand total", "opening balance", "total", "cr"]):
                noise_idx.append(i)

        if noise_idx:
            df = df.drop(index=noise_idx).copy()

        # If columns are raw integers or unnamed, auto-detect header row
        unnamed_or_int = 0
        for c in df.columns:
            s_c = str(c).strip().lower()
            if s_c.startswith("unnamed") or s_c.isdigit() or isinstance(c, int):
                unnamed_or_int += 1

        if unnamed_or_int >= max(1, len(df.columns) * 0.5):
            # Check if early rows already contain transaction dates.
            # If so, the table contains direct data rows without a leading header row.
            early_date_count = 0
            for r_idx in range(min(5, len(df))):
                first_cell = str(df.iloc[r_idx, 0]).strip()
                if self.is_valid_date(first_cell):
                    early_date_count += 1

            if early_date_count < 2:
                best_row, score = self.find_best_header_row(df)
                if score >= 3:
                    new_headers = [str(h).strip() for h in df.iloc[best_row].values]
                    df = df.iloc[best_row + 1:].copy()
                    df.columns = new_headers

        # Ensure unique column names to avoid duplicate index DataFrame conversions
        seen_cols = {}
        unique_cols = []
        for i, c in enumerate(df.columns):
            c_str = str(c).strip()
            if not c_str or c_str in seen_cols:
                seen_cols[c_str] = seen_cols.get(c_str, 0) + 1
                unique_cols.append(f"{c_str}_{seen_cols[c_str]}")
            else:
                seen_cols[c_str] = 1
                unique_cols.append(c_str)
        df.columns = unique_cols

        # Drop entirely blank rows & columns
        df.dropna(how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)

        col_map = self.map_columns(list(df.columns))
        date_col = col_map["date_col"]
        desc_col = col_map["desc_col"]
        debit_col = col_map["debit_col"]
        credit_col = col_map["credit_col"]
        amt_col = col_map["amt_col"]
        type_col = col_map["type_col"]
        ref_col = col_map["ref_col"]

        has_debit_credit = (debit_col is not None and credit_col is not None)
        has_amount = (amt_col is not None or debit_col is not None)

        # Fallback: Automatic Data-Driven Column Type Detection if named headers were missing
        if not has_amount and not has_debit_credit:
            col_scores = {}
            for c in df.columns:
                series = df[c].dropna().astype(str).str.strip()
                non_empty = [v for v in series if v and v.lower() not in ("nan", "none", "-", "", "null")]
                if not non_empty:
                    continue
                date_count = sum(1 for v in non_empty if self.is_valid_date(v))
                amount_count = 0
                for v in non_empty:
                    if self.is_valid_date(v):
                        continue
                    cleaned_num = re.sub(r"[^\d.,\-+]", "", v.strip())
                    digits_only = re.sub(r"\D", "", cleaned_num)
                    # Filter out non-numeric strings, phone numbers (>11 digits), or empty strings
                    if cleaned_num and not cleaned_num.startswith("+91") and 1 <= len(digits_only) <= 10:
                        try:
                            val = self.clean_amount(cleaned_num)
                            if 0.0 < val < 100_000_000:
                                amount_count += 1
                        except Exception:
                            pass
                avg_len = sum(len(v) for v in non_empty) / max(1, len(non_empty))
                col_scores[c] = {
                    "date_pct": date_count / len(non_empty),
                    "amount_pct": amount_count / len(non_empty),
                    "avg_len": avg_len
                }

            # 1. Identify date column if missing
            if not date_col and col_scores:
                best_date = max(col_scores.items(), key=lambda x: x[1]["date_pct"], default=(None, {}))
                if best_date[1] and best_date[1].get("date_pct", 0) >= 0.15:
                    date_col = best_date[0]

            # 2. Identify amount/debit/credit columns
            amount_candidates = [c for c, sc in col_scores.items() if sc["amount_pct"] >= 0.15 and c != date_col]
            if not amount_candidates:
                # Fallback to column with highest amount_pct that is not date_col
                non_date_cols = [c for c in col_scores.keys() if c != date_col]
                if non_date_cols:
                    best_amt_candidate = max(non_date_cols, key=lambda c: col_scores[c]["amount_pct"])
                    if col_scores[best_amt_candidate]["amount_pct"] > 0:
                        amount_candidates = [best_amt_candidate]

            if amount_candidates:
                if len(amount_candidates) == 1:
                    amt_col = amount_candidates[0]
                    has_amount = True
                elif len(amount_candidates) == 2:
                    debit_col = amount_candidates[0]
                    credit_col = amount_candidates[1]
                    has_debit_credit = True
                elif len(amount_candidates) >= 3:
                    # In standard bank tables [Debit, Credit, Balance], first is Debit, second is Credit, third is Balance
                    debit_col = amount_candidates[0]
                    credit_col = amount_candidates[1]
                    has_debit_credit = True

            # 3. Identify description column (longest text column not mapped to date or amounts)
            if not desc_col and col_scores:
                remaining = [c for c in col_scores.keys() if c != date_col and c not in amount_candidates]
                if remaining:
                    desc_col = max(remaining, key=lambda c: col_scores[c]["avg_len"])

            has_debit_credit = (debit_col is not None and credit_col is not None)
            has_amount = (amt_col is not None or debit_col is not None)

        if not has_amount and not has_debit_credit:
            raise ValueError(
                f"Could not automatically detect transaction amount or debit/credit columns. "
                f"Columns found: {list(df.columns)}. Please verify your file format."
            )

        transactions: List[Dict[str, Any]] = []

        for idx, row in df.iterrows():
            row_str_vals = [self.clean_text(v) for v in row.values]

            # 1. Skip summary / footer noise lines
            if self.is_noise_row(row_str_vals):
                continue

            raw_date = self.clean_text(row[date_col]) if date_col and pd.notna(row.get(date_col)) else ""
            raw_desc = self.clean_text(row[desc_col]) if desc_col and pd.notna(row.get(desc_col)) else ""
            raw_ref = self.clean_text(row[ref_col]) if ref_col and pd.notna(row.get(ref_col)) else ""

            # 2. Extract debit and credit amounts
            debit_val = 0.0
            credit_val = 0.0
            is_debit = False

            if has_debit_credit:
                debit_val = self.clean_amount(row[debit_col])
                credit_val = self.clean_amount(row[credit_col])
                if debit_val > 0:
                    is_debit = True
            elif type_col and amt_col:
                raw_amt = self.clean_amount(row[amt_col])
                type_val = self.clean_text(row[type_col]).upper()
                if any(k in type_val for k in ["DR", "DEBIT", "WDL", "WITHDRAWAL"]):
                    debit_val = raw_amt
                    is_debit = True
                else:
                    credit_val = raw_amt
            elif amt_col:
                cell_raw = str(row[amt_col]).strip()
                parsed_amt = self.clean_amount(cell_raw)
                if "-" in cell_raw or "dr" in cell_raw.lower() or "wdl" in cell_raw.lower():
                    debit_val = parsed_amt
                    is_debit = True
                elif "cr" in cell_raw.lower() or "dep" in cell_raw.lower():
                    credit_val = parsed_amt
                else:
                    debit_val = parsed_amt
                    is_debit = True
            elif debit_col:
                debit_val = self.clean_amount(row[debit_col])
                is_debit = (debit_val > 0)

            # 3. Continuation lines
            if not raw_date and debit_val == 0.0 and credit_val == 0.0:
                if transactions and raw_desc:
                    transactions[-1]["description"] += " " + raw_desc
                continue

            # Validate date format (reject metadata rows that place balances in the date field)
            if raw_date and not self.is_valid_date(raw_date):
                continue

            # 4. Filter for debits/expenditures (the primary fraud risk surface)
            if not is_debit or debit_val <= 0.0:
                continue

            # 5. Clean description fallback
            if not raw_desc:
                raw_desc = f"Transaction on {raw_date}" if raw_date else f"Transaction #{len(transactions)+1}"

            transactions.append({
                "date": raw_date if raw_date else "Recent",
                "description": raw_desc,
                "amount": debit_val,
                "ref_no": raw_ref
            })

        return transactions

    def scan_file(self, file_bytes: bytes, filename: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Universal entrypoint: Unlocks, parses, standardizes, and evaluates any bank statement
        against the PyTorch Deep Focal Neural Network model.
        """
        df_raw = self.extract_file_content(file_bytes, filename, password)
        parsed_txns = self.parse_statement_dataframe(df_raw)

        if not parsed_txns:
            raise ValueError(
                "No valid debit transactions were detected in the statement. "
                "Please ensure the file contains transaction records."
            )

        # Baseline consumer spending median for anomaly scoring (resistant to fraud outliers)
        amounts = [t["amount"] for t in parsed_txns]
        user_avg = float(pd.Series(amounts).median()) if amounts else 50.0

        features_list = []
        meta_list = []

        for idx, t in enumerate(parsed_txns):
            raw_amt = t["amount"]
            desc = t["description"]
            date_val = t["date"]
            cat_val = self.infer_category(desc)

            d_lower = desc.lower()
            is_foreign = any(k in d_lower for k in [
                "intl", "overseas", "foreign", "london", "singapore", "dubai",
                "lagos", "uk", "us", "eu", "international", "usd", "gbp", "eur", "aed"
            ])
            is_night = any(k in d_lower for k in [
                "01:", "02:", "03:", "04:", "midnight", "atm-midnight"
            ])

            channel = (
                "atm" if cat_val == "atm"
                else "online" if any(k in d_lower for k in ["upi", "neft", "imps", "online", "pay", ".com", "www", "net", "e-com", "app"])
                else "in_store_chip"
            )

            # Map to model's 29-dimensional behavioral latent space
            scaled_feats = self.mapper.map_to_features(
                amount=raw_amt,
                merchant_category=cat_val,
                channel=channel,
                is_foreign=is_foreign,
                is_night_time=is_night,
                device_trusted=True,
                user_avg_amount=user_avg,
                velocity_1h=1
            )
            features_list.append(scaled_feats)
            meta_list.append((raw_amt, desc, date_val, cat_val, channel, is_foreign, is_night))

        # Batched inference across entire statement in a single forward pass
        batch_feats = np.vstack(features_list)
        preds = self.predictor.predict_batch(batch_feats)

        results: List[Dict[str, Any]] = []
        for idx, (pred, meta) in enumerate(zip(preds, meta_list)):
            raw_amt, desc, date_val, cat_val, channel, is_foreign, is_night = meta
            expl = TransactionExplainer.generate_explanation(
                amount=raw_amt,
                merchant_category=cat_val,
                channel=channel,
                is_foreign=is_foreign,
                is_night_time=is_night,
                device_trusted=True,
                user_avg_amount=user_avg,
                velocity_1h=1,
                prediction_result=pred
            )

            results.append({
                "id": idx + 1,
                "date": date_val,
                "description": desc,
                "category": cat_val,
                "amount": raw_amt,
                "risk_score_percent": pred["risk_score_percent"],
                "status": pred["status"],
                "risk_tier": pred["risk_tier"],
                "theme": pred["theme"],
                "top_reason": expl["risk_factors"][0]["title"] if expl["risk_factors"] else "Verified normal spending"
            })

        total_txns = len(results)
        blocked_txns = sum(1 for r in results if r["status"] == "BLOCKED")
        challenged_txns = sum(1 for r in results if r["status"] == "CHALLENGE")
        approved_txns = sum(1 for r in results if r["status"] == "APPROVED")
        total_spend = sum(r["amount"] for r in results)
        flagged_amount = sum(r["amount"] for r in results if r["status"] in ["BLOCKED", "CHALLENGE"])

        return {
            "summary": {
                "total_transactions": total_txns,
                "approved_count": approved_txns,
                "challenged_count": challenged_txns,
                "blocked_count": blocked_txns,
                "total_volume_dollars": round(total_spend, 2),
                "flagged_volume_dollars": round(flagged_amount, 2),
                "account_health": (
                    "Healthy" if blocked_txns == 0 and challenged_txns <= 1
                    else "At Risk" if blocked_txns > 0
                    else "Review Needed"
                )
            },
            "transactions": results
        }
