# bank_column_map.py

# Canonical internal schema (DO NOT CHANGE lightly)
CANONICAL_COLS = ["date", "particulars", "dr", "cr", "balance"]

BANK_COLUMN_MAP = {
    "Axis Bank": {
        "date": "Tran Date",
        "particulars": "PARTICULARS",
        "dr": "DR",
        "cr": "CR",
        "balance": "BAL",
    },
    "SBI Bank": {
        "date": "Date",
        "particulars": "Details",
        "dr": "Debit",
        "cr": "Credit",
        "balance": "Balance",
    },
    "Union Bank": {
        "date": "Date",
        "particulars": "Remarks",
        "dr": "Withdrawals",
        "cr": "Deposits",
        "balance": "Balance",
    },
    "South Indian Bank": {
        "date": "DATE",
        "particulars": "PARTICULARS",
        "dr": "WITHDRAWALS",
        "cr": "DEPOSITS",
        "balance": "BALANCE",
    },
    "ICICI Bank": {
        "date": "Transaction Date",
        "particulars": "Transaction Remarks",
        "dr": "Withdrawal Amount (INR )",
        "cr": "Deposit Amount (INR )",
        "balance": "Balance (INR )",
    },

}


