import pandas as pd
from statement_ingestion_core.bank_parser import parse_bank_csv

def normalize_to_canonical(df, bank_name):
    COLUMN_MAP = {
        # date
        "Tran Date": "date",
        "Transaction Date": "date",
        "Transaction_Date": "date",
        "Date": "date",

        # particulars
        "PARTICULARS": "particulars",
        "Particulars": "particulars",
        "Description": "particulars",
        "Narration": "particulars",

        # debit
        "Debit": "dr",
        "Withdrawal": "dr",
        "Withdrawals": "dr",
        "DR": "dr",

        # credit
        "Credit": "cr",
        "Deposit": "cr",
        "Deposits": "cr",
        "CR": "cr",

        # bank
        "Bank": "bank",
    }

    df = df.rename(columns={
        col: COLUMN_MAP[col]
        for col in df.columns
        if col in COLUMN_MAP
    })

    df = df.loc[:, ~df.columns.duplicated()]
    df["bank"] = bank_name
    df["date"] = df["date"].astype(str)

    required = ["date", "particulars", "dr", "cr", "bank"]
    return df[required]

def parse_to_canonical(csv_path: str, bank_name: str) -> pd.DataFrame:
    """
    UI-agnostic ingestion.
    CSV → canonical DataFrame
    """
    df = parse_bank_csv(csv_path, bank_name)
    df = normalize_to_canonical(df, bank_name)
    return df

