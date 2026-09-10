"""
Extract the "data center protests" sub-dataset from the ACLED US events file.

Source: data/raw/ACLED_US_events_from_2024-01-01_event_date_to_2026-09-08.csv
Method: keyword match on `notes` (free text) for "data center" / "data centre",
since the `tags` column only carries crowd-size / repression flags, not topic.
"""
import pandas as pd

SRC = "data/raw/ACLED_US_events_from_2024-01-01_event_date_to_2026-09-08.csv"
OUT = "data/source/us_data_center_protests.csv"

df = pd.read_csv(SRC)
notes = df["notes"].fillna("").str.lower()  # lowercase to catch "Data Center" / "DATA CENTER" too
mask = notes.str.contains("data center") | notes.str.contains("data centre")
subset = df[mask].copy()  # keeps all 31 original columns, no field dropped

subset.to_csv(OUT, index=False)
print(f"Extracted {len(subset)} / {len(df)} rows -> {OUT}")
