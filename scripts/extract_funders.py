#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas", "openpyxl"]
# ///
"""Extract funder data from Excel file."""

import pandas as pd
from pathlib import Path

# File path
excel_file = Path(__file__).parent.parent / "Future of Open Environmental Data Convening Guest List - September 2025.xlsx"

# Load FINAL ATTENDANCE tab
print("Loading FINAL ATTENDANCE tab...")
df = pd.read_excel(excel_file, sheet_name="FINAL ATTENDANCE")

print(f"✓ Loaded {len(df)} rows")
print("\nColumns:", df.columns.tolist())
print("\nAll affiliations:")
for idx, row in df.iterrows():
    affiliation = row.get('Affiliation ', 'N/A')
    print(f"{idx:2d}. {affiliation}")
