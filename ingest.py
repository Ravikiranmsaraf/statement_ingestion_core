from statement_ingestion_core.canonical import CANONICAL_COLUMNS, CANONICAL_ORDER    
from statement_ingestion_core.bank_column_map import BANK_COLUMN_MAP
from statement_ingestion_core.bank_parser import parse_bank_csv
from statement_ingestion_core.mapper import map_to_canonical
from statement_ingestion_core.sanitizer import sanitize_canonical

from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class IngestionResult:
    raw_df: pd.DataFrame
    canonical_df: pd.DataFrame
    bank: str

def ingest_statement(path: str, bank: str) -> IngestionResult:
    raw_df = parse_bank_csv(path, bank)

    canonical_df = map_to_canonical(
        raw_df,
        bank,
        BANK_COLUMN_MAP[bank]
    )
    canonical_df = sanitize_canonical(canonical_df)

    return IngestionResult(
        raw_df=raw_df,
        canonical_df=canonical_df,
        bank=bank
    )
# ---------------------------------
def parse_to_canonical(path, bank):
    raw_df = parse_bank_csv(path, bank)

    canon_df = map_to_canonical(
        raw_df,
        bank,
        BANK_COLUMN_MAP[bank]
    )

    canon_df = sanitize_canonical(canon_df)
    return canon_df[CANONICAL_ORDER]
