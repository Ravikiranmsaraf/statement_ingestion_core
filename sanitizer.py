#sanitizer.py
import pandas as pd
def sanitize_canonical(df):
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date"])

    df["particulars"] = df["particulars"].fillna("").astype(str)
    df["dr"] = pd.to_numeric(df["dr"], errors="coerce").fillna(0.0)
    df["cr"] = pd.to_numeric(df["cr"], errors="coerce").fillna(0.0)

    df = df[(df["dr"] != 0) | (df["cr"] != 0)]
    return df
