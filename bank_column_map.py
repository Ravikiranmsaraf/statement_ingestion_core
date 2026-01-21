# bank_column_map.py
"""
Bank → Canonical column mappings.

Rules:
- Keys = canonical column names (DO NOT CHANGE lightly)
- Values = list of possible column names from bank CSVs
- Order matters: first match wins
- This file must contain ZERO logic
"""

# -----------------------------
# Canonical internal schema
# -----------------------------
CANONICAL_COLUMNS = [
    "date",
    "particulars",
    "dr",
    "cr",
    "bank",
]

CANONICAL_ORDER = [
    "date",
    "particulars",
    "dr",
    "cr",
    "bank",
]

# -----------------------------
# Bank-specific column aliases
# -----------------------------
BANK_COLUMN_MAP = {

    "Axis Bank": {
        "date": ["Tran Date", "Transaction Date"],
        "particulars": ["PARTICULARS", "Particulars", "Narration"],
        "dr": ["DR", "Debit"],
        "cr": ["CR", "Credit"],
    },

    "SBI Bank": {
        "date": ["Date", "Transaction Date"],
        "particulars": ["Details", "Narration", "Description"],
        "dr": ["Debit"],
        "cr": ["Credit"],
    },

    "Union Bank": {
        "date": ["Date", "Transaction Date"],
        "particulars": ["Remarks", "Narration", "Particulars"],
        "dr": ["Withdrawals", "Debit"],
        "cr": ["Deposits", "Credit"],
    },

    "South Indian Bank": {
        "date": ["DATE"],
        "particulars": ["PARTICULARS", "Narration"],
        "dr": ["WITHDRAWALS"],
        "cr": ["DEPOSITS"],
    },

    "ICICI Bank": {
        "date": ["Transaction Date", "Value Date"],
        "particulars": ["Transaction Remarks", "Narration"],
        "dr": ["Withdrawal Amount (INR )"],
        "cr": ["Deposit Amount (INR )"],
    },
}
