# mapper.py
import pandas as pd

def map_to_canonical(df, bank_name, bank_map):
    out = {}

    for canon_col, aliases in bank_map.items():
        for col in aliases:
            if col in df.columns:
                out[canon_col] = df[col]
                break
        else:
            out[canon_col] = None

    canon_df = pd.DataFrame(out)
    canon_df["bank"] = bank_name
    return canon_df
