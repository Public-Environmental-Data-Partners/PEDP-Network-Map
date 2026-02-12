#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas", "openpyxl"]
# ///
"""Generate funders CSV from PEDP Funder spreadsheet."""

import pandas as pd
from pathlib import Path
import re

# File paths
excel_file = Path(__file__).parent.parent / "PEDP Funder spreadsheet.xlsx"
output_file = Path(__file__).parent.parent / "data" / "funders_to_add.csv"

# Load Funder List sheet
print("Loading Funder List sheet...")
df = pd.read_excel(excel_file, sheet_name="Funder List")
print(f"✓ Loaded {len(df)} rows\n")

funders = []

for idx, row in df.iterrows():
    funder_name = str(row.get('Funder', '')).strip()
    status = str(row.get('Status ', '')).strip()

    # Skip empty rows
    if pd.isna(funder_name) or funder_name == 'nan' or funder_name == '':
        continue

    # Generate ID (remove special chars, spaces, limit length)
    org_id = re.sub(r'[^a-zA-Z]', '', funder_name.replace(' ', ''))[:20]

    # Get program/interest for description
    program = row.get('Program', '')
    interest = row.get('Funder interest', '')
    desc_parts = []
    if pd.notna(program) and program != '':
        desc_parts.append(f"Program: {program}")
    if pd.notna(interest) and str(interest) != 'nan' and interest != '':
        interest_str = str(interest)[:100]  # Truncate long descriptions
        desc_parts.append(f"Interest: {interest_str}")

    description = '; '.join(desc_parts) if desc_parts else 'Funder interested in environmental data initiatives'

    # Clean up status
    if pd.isna(status) or status == 'nan':
        status = '0. On our radar'

    funders.append({
        'id': org_id,
        'name': funder_name,
        'organization': funder_name,
        'contact': '',
        'description': description,
        'status': status,
        'website': '',
        'category': 'Funder',
        'timeline': 'Established/Long-running',
        'color': 'teal'
    })

# Create DataFrame
funders_df = pd.DataFrame(funders)

# Save to CSV
funders_df.to_csv(output_file, index=False)

print(f"✓ Generated {len(funders_df)} funders")
print(f"✓ Saved to: {output_file}\n")

# Show summary by status
print("=" * 70)
print("FUNDER STATUS SUMMARY")
print("=" * 70)

status_counts = funders_df['status'].value_counts()
for status, count in status_counts.items():
    print(f"\n{status}: {count} funders")
    funders_in_status = funders_df[funders_df['status'] == status]
    for idx, funder in funders_in_status.iterrows():
        if '4' in status or 'approved' in status.lower():
            print(f"  ✓ {funder['name']:40s} → will fund PEDP")
        else:
            print(f"  • {funder['name']}")

print("\n" + "=" * 70)
print("Next step: Copy these rows into your Google Sheet Nodes tab")
print("=" * 70)
