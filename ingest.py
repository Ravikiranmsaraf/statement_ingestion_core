import pandas as pd
from statement_ingestion_core.canonical import CANONICAL_COLUMNS,CANONICAL_ORDER    
from statement_ingestion_core.bank_column_map import BANK_COLUMN_MAP
from statement_ingestion_core.bank_parser import parse_bank_csv
from statement_ingestion_core.mapper import map_to_canonical
from statement_ingestion_core.sanitizer import sanitize_canonical

# def normalize_to_canonical(df, bank_name):
#     COLUMN_MAP = {
#         # date
#         "Tran Date": "date",
#         "Transaction Date": "date",
#         "Transaction_Date": "date",
#         "Date": "date",

#         # particulars
#         "PARTICULARS": "particulars",
#         "Particulars": "particulars",
#         "Description": "particulars",
#         "Narration": "particulars",
#         "Details": "particulars",
#         "Remarks": "particulars",
#         "Transaction Remarks": "particulars",

#         # debit
#         "Debit": "dr",
#         "Withdrawal": "dr",
#         "Withdrawals": "dr",
#         "DR": "dr",

#         # credit
#         "Credit": "cr",
#         "Deposit": "cr",
#         "Deposits": "cr",
#         "CR": "cr",
#     }

#     df = df.rename(columns={c: COLUMN_MAP[c] for c in df.columns if c in COLUMN_MAP})
#     df = df.loc[:, ~df.columns.duplicated()]
#     df["bank"] = bank_name

#     # --- date ---
#     df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
#     df = df.dropna(subset=["date"])
#     df["date"] = df["date"].dt.strftime("%Y-%m-%d")

#     # --- amounts ---
#     for col in ["dr", "cr"]:
#         df[col] = (
#             df[col]
#             .astype(str)
#             .str.replace(",", "", regex=False)
#             .str.strip()
#             .replace("", "0")
#             .astype(float)
#         )

#     # ✅ MATCH OLD data_processor.py BEHAVIOR
#     df["particulars"] = df["particulars"].fillna("")
#     df["dr"] = df["dr"].fillna(0.0)
#     df["cr"] = df["cr"].fillna(0.0)

#     # ✅ FILTER NON-TRANSACTION ROWS
#     df = df[(df["dr"] != 0) | (df["cr"] != 0)]

#     required = ["date", "particulars", "dr", "cr", "bank"]
#     return df[required]


# def parse_to_canonical(csv_path: str, bank_name: str) -> pd.DataFrame:
#     """
#     UI-agnostic ingestion.
#     CSV → canonical DataFrame
#     """
#     df = parse_bank_csv(csv_path, bank_name)
#     df = normalize_to_canonical(df, bank_name)
#     return df

def parse_to_canonical(path, bank):
    raw_df = parse_bank_csv(path, bank)

    canon_df = map_to_canonical(
        raw_df,
        bank,
        BANK_COLUMN_MAP[bank]
    )

    canon_df = sanitize_canonical(canon_df)
    return canon_df[CANONICAL_ORDER]
