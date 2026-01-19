import pandas as pd
from statement_ingestion_core.bank_parser import parse_bank_csv

def parse_to_canonical(csv_path: str, bank_name: str) -> pd.DataFrame:
    """
    UI-agnostic ingestion.
    CSV → canonical DataFrame
    """
    return parse_bank_csv(csv_path, bank_name)
