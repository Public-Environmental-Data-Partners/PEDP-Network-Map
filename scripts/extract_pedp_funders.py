#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas", "openpyxl"]
# ///
"""Extract funder data from PEDP Funder spreadsheet."""

import pandas as pd
from pathlib import Path

# File path
excel_file = Path(__file__).parent.parent / "PEDP Funder spreadsheet.xlsx"

# Load Funder List sheet
print("Loading Funder List sheet...")
df = pd.read_excel(excel_file, sheet_name="Funder List")

print(f"✓ Loaded {len(df)} rows")
print("\nColumns:", df.columns.tolist())
print("\nFirst 15 rows:")
print(df.head(15).to_string())
print("\n...")
