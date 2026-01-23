#sanitizer.py
import pandas as pd

def sanitize_canonical(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Own the dataframe (CRITICAL)
    df = df.copy()

    # 2. Date normalization
    df.loc[:, "date"] = pd.to_datetime(
        df["date"], dayfirst=True, errors="coerce"
    )
    df = df.dropna(subset=["date"]).copy()

    # 3. Text + numeric sanitization
    df.loc[:, "particulars"] = (
        df["particulars"]
        .fillna("")
        .astype(str)
    )

    df.loc[:, "dr"] = (
        pd.to_numeric(df["dr"], errors="coerce")
        .fillna(0.0)
    )

    df.loc[:, "cr"] = (
        pd.to_numeric(df["cr"], errors="coerce")
        .fillna(0.0)
    )

    # 4. Remove zero-value rows
    df = df[(df["dr"] != 0) | (df["cr"] != 0)].copy()

    return df
