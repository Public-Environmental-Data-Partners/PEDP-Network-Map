#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas", "openpyxl"]
# ///
"""Generate funders CSV from Excel file."""

import pandas as pd
from pathlib import Path
import re

# File paths
excel_file = Path(__file__).parent.parent / "Future of Open Environmental Data Convening Guest List - September 2025.xlsx"
output_file = Path(__file__).parent.parent / "data" / "funders_to_add.csv"

# Load FINAL ATTENDANCE tab
print("Loading FINAL ATTENDANCE tab...")
df = pd.read_excel(excel_file, sheet_name="FINAL ATTENDANCE")
print(f"✓ Loaded {len(df)} rows")

# Identify funders by keywords in affiliation
funder_keywords = [
    'foundation', 'fund', 'trust', 'philanthropies', 'philanthropy',
    'project', 'initiative', 'center', 'simons', '11th hour',
    'moore', 'pew', 'kapor', 'heising', 'aspen', 'schmidt'
]

funders = []
seen_orgs = set()

for idx, row in df.iterrows():
    affiliation = str(row.get('Affiliation ', '')).strip()

    if pd.isna(affiliation) or affiliation == 'nan' or affiliation == '':
        continue

    # Check if this looks like a funder
    is_funder = any(keyword in affiliation.lower() for keyword in funder_keywords)

    if is_funder:
        # Clean up the name
        org_name = affiliation.strip()

        # Skip duplicates
        if org_name in seen_orgs:
            continue
        seen_orgs.add(org_name)

        # Generate ID (first word or first 2 words, clean)
        id_parts = org_name.split()[:2]
        org_id = ''.join(re.sub(r'[^a-zA-Z]', '', word) for word in id_parts)

        # Determine status (default to conversation)
        # Moore Foundation is known approved funder
        if 'moore' in org_name.lower():
            status = '4. approved'
        elif '11th hour' in org_name.lower():
            status = '4. approved'
        else:
            status = '1. In conversation'

        funders.append({
            'id': org_id,
            'name': org_name,
            'organization': org_name,
            'contact': '',
            'description': f'Funder interested in environmental data initiatives',
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

print(f"\n✓ Generated {len(funders_df)} funders")
print(f"✓ Saved to: {output_file}\n")

print("Funders extracted:")
for idx, row in funders_df.iterrows():
    print(f"  • {row['name']:40s} status: {row['status']}")

print("\n" + "="*60)
print("Next step: Copy these rows into your Google Sheet Nodes tab")
print("="*60)
