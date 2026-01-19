import pandas as pd
import re

def _safe_float(v):
    try:
        return float(str(v).replace(",", "").strip())
    except:
        return 0.0

def _clean_text(s):
    if pd.isna(s):
        return ""
    s = str(s).upper()
    s = re.sub(r"[^A-Z0-9\s\-/\.]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_axis(df):
    return [
        {
            "text": _clean_text(row.get("Particulars")),
            "debit": _safe_float(row.get("Debit")),
            "credit": _safe_float(row.get("Credit")),
        }
        for _, row in df.iterrows()
    ]



def parse_sbi(df):
    def clean_sbi(text):
        if not isinstance(text, str):
            return text
        text = text.replace("\n", " ").replace("\r", " ")
        text = re.sub(r"^\s*(WDL\s+TFR|DEP\s+TFR)\s+", "", text, flags=re.I)
        return text

    return [
        {
            "text": _clean_text(clean_sbi(row.get("Particulars"))),
            "debit": _safe_float(row.get("Debit")),
            "credit": _safe_float(row.get("Credit")),
        }
        for _, row in df.iterrows()
    ]


def parse_union(df):
    return [
        {
            "text": _clean_text(row.get("Remarks") or row.get("Particulars")),
            "debit": _safe_float(row.get("Withdrawals") or row.get("Debit")),
            "credit": _safe_float(row.get("Deposits") or row.get("Credit")),
        }
        for _, row in df.iterrows()
    ]


def parse_south_indian(df):
    return [
        {
            "text": _clean_text(row.get("PARTICULARS")),
            "debit": _safe_float(row.get("WITHDRAWALS")),
            "credit": _safe_float(row.get("DEPOSITS")),
        }
        for _, row in df.iterrows()
    ]

def parse_icici(df):
    return [
        {
            "text": _clean_text(row.get("Transaction Remarks")),
            "debit": _safe_float(row.get("Withdrawal Amount (INR )")),
            "credit": _safe_float(row.get("Deposit Amount (INR )")),
        }
        for _, row in df.iterrows()
    ]



PARSER_DISPATCH = {
    "Axis Bank": parse_axis,
    "SBI Bank": parse_sbi,
    "Union Bank": parse_union,
    "South Indian Bank": parse_south_indian,
    "ICICI Bank": parse_icici,
}


def parse_bank(df, bank_name):
    if bank_name not in PARSER_DISPATCH:
        raise ValueError("Unsupported bank selected")
    return PARSER_DISPATCH[bank_name](df)
