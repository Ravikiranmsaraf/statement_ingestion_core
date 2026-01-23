import pandas as pd
import io
import re
from difflib import get_close_matches

# bank_parser.py

BANK_HEADER_ANCHORS = {
    "Axis Bank": ["Tran Date", "PARTICULARS", "DR", "CR"],
    "SBI Bank": ["Date", "Details", "Debit", "Credit"],
    "Union Bank": ["Date", "Remarks", "Withdrawals", "Deposits"],
        # NEW
    "South Indian Bank": ["DATE", "PARTICULARS", "WITHDRAWALS", "DEPOSITS"],
    "ICICI Bank": ["Value Date", "Transaction Date", "Withdrawal Amount", "Deposit Amount"],
}


# ---------------------------------
# 1. VALIDATION + HEADER DETECTION
# ---------------------------------

def get_validated_df(file_path, bank_name):
    import pandas as pd
    import io
    import re

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    bank_anchors = BANK_HEADER_ANCHORS[bank_name]

    header_row_index = None
    for i, line in enumerate(lines):
        if sum(a.lower() in line.lower() for a in bank_anchors) >= 2:
            header_row_index = i
            break

    if header_row_index is None:
        raise RuntimeError("Transaction table header not found")

    meta_lines = lines[:header_row_index]
    table_lines = lines[header_row_index:]

    meta_df = pd.DataFrame({"__meta__": meta_lines})

    # -------------------------------------------------
    # ✅ Axis / Union: parse directly (NO stitching)
    # -------------------------------------------------
    if bank_name != "SBI Bank":
        table_buffer = io.StringIO("".join(table_lines))
        txn_df = pd.read_csv(
            table_buffer,
            engine="python",
            on_bad_lines="skip"
        )
        txn_df.attrs["statement_meta_df"] = meta_df
        return txn_df

    # -------------------------------------------------
    # ✅ SBI: column-count safe stitching
    # -------------------------------------------------
    header = table_lines[0].rstrip("\n")
    expected_cols = len(header.split(","))

    stitched = []
    buffer = ""

    for line in table_lines[1:]:
        buffer = buffer + " " + line.strip() if buffer else line.rstrip("\n")

        try:
            pd.read_csv(io.StringIO(header + "\n" + buffer))
            stitched.append(buffer)
            buffer = ""
        except Exception:
            continue

    if buffer:
        stitched.append(buffer)

    final_lines = [header] + stitched
    table_buffer = io.StringIO("\n".join(final_lines))

    txn_df = pd.read_csv(
        table_buffer,
        engine="python"
    )

    txn_df.attrs["statement_meta_df"] = meta_df
    return txn_df


# ---------------------------------
# 4. CLEAN & STANDARDIZE (INTERNAL)
# ---------------------------------
def clean_and_standardize(df: pd.DataFrame, bank_name: str) -> pd.DataFrame:
    attrs = df.attrs.copy()   # SAVE METADATA

    for col in ['Debit', 'Credit', 'Running_Balance']:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '', regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0.0

    df['Bank'] = bank_name

    df = df.reset_index(drop=True)
    df.attrs = attrs          # RESTORE METADATA
    return df


# ---------------------------------
# 5. PUBLIC ENTRY POINT (USED BY UI)
# ---------------------------------
def parse_bank_csv(file_path: str, bank_name: str) -> pd.DataFrame:
    df = get_validated_df(file_path, bank_name)

    df.attrs["statement_meta_df"] = df.attrs.get("statement_meta_df")
    df.attrs["raw_columns"] = list(df.columns)
    df.attrs["bank_name"] = bank_name

    # _assert_csv_integrity(df, bank_name)  # 🔒 regression guard

    return clean_and_standardize(df, bank_name)

