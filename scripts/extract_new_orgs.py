#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas", "openpyxl"]
# ///
"""Extract new organizations from attendance list that aren't already in nodes."""

import pandas as pd
from pathlib import Path
import re

# File paths
attendance_file = Path(__file__).parent.parent / "Future of Open Environmental Data Convening Guest List - September 2025.xlsx"
nodes_file = Path(__file__).parent.parent / "data" / "processed" / "nodes.csv"
funders_file = Path(__file__).parent.parent / "data" / "funders_to_add.csv"
output_file = Path(__file__).parent.parent / "data" / "new_orgs_to_add.csv"

# Load existing data
print("Loading existing nodes and funders...")
existing_nodes = pd.read_csv(nodes_file)
existing_funders = pd.read_csv(funders_file)

# Combine to get all known organizations
all_known_orgs = set()
for df in [existing_nodes, existing_funders]:
    all_known_orgs.update(df['name'].str.lower().str.strip())
    all_known_orgs.update(df['organization'].str.lower().str.strip())

print(f"✓ Found {len(all_known_orgs)} known organizations\n")

# Load attendance list
print("Loading FINAL ATTENDANCE...")
attendance_df = pd.read_excel(attendance_file, sheet_name="FINAL ATTENDANCE")
print(f"✓ Loaded {len(attendance_df)} attendees\n")

# Extract unique organizations
attendee_orgs = []
for idx, row in attendance_df.iterrows():
    affiliation = str(row.get('Affiliation ', '')).strip()

    if pd.isna(affiliation) or affiliation == 'nan' or affiliation == '':
        continue

    attendee_orgs.append(affiliation)

unique_attendee_orgs = set(attendee_orgs)
print(f"Found {len(unique_attendee_orgs)} unique organizations in attendance list\n")

# Find NEW organizations (not in existing nodes or funders)
new_orgs = []
for org in sorted(unique_attendee_orgs):
    org_lower = org.lower().strip()

    # Check if this org is already known
    is_known = False
    for known_org in all_known_orgs:
        if org_lower in known_org or known_org in org_lower:
            is_known = True
            break

    if not is_known:
        new_orgs.append(org)

print(f"✓ Found {len(new_orgs)} NEW organizations not in existing data\n")

# Generate CSV entries for new orgs
new_nodes = []
for org in new_orgs:
    # Generate ID
    org_id = re.sub(r'[^a-zA-Z]', '', org.replace(' ', ''))[:20]

    # Determine category based on keywords
    org_lower = org.lower()
    if any(word in org_lower for word in ['university', 'college', 'lab', 'institute', 'school']):
        category = 'Research/Academic'
        color = 'blue'
    elif any(word in org_lower for word in ['government', 'agency', 'epa', 'usgs', 'noaa', 'state', 'federal']):
        category = 'Government/Agency'
        color = 'orange'
    elif any(word in org_lower for word in ['archive', 'library']):
        category = 'Data Preservation/Archiving'
        color = 'green'
    elif any(word in org_lower for word in ['data', 'tech', 'digital']):
        category = 'Data Coordination/Standards'
        color = 'red'
    else:
        category = 'Capacity Building/Support'
        color = 'orange'

    new_nodes.append({
        'id': org_id,
        'name': org,
        'organization': org,
        'contact': '',
        'description': f'Organization from Future of Open Environmental Data Convening (Sept 2025)',
        'status': 'Established',
        'website': '',
        'category': category,
        'timeline': 'Established/Long-running',
        'color': color
    })

# Create DataFrame and save
new_nodes_df = pd.DataFrame(new_nodes)
new_nodes_df.to_csv(output_file, index=False)

print(f"✓ Generated {len(new_nodes_df)} new organization entries")
print(f"✓ Saved to: {output_file}\n")

# Show summary
print("=" * 70)
print("NEW ORGANIZATIONS TO ADD")
print("=" * 70)

category_counts = new_nodes_df['category'].value_counts()
for category, count in category_counts.items():
    print(f"\n{category}: {count} organizations")
    orgs_in_cat = new_nodes_df[new_nodes_df['category'] == category]
    for idx, org in orgs_in_cat.iterrows():
        print(f"  • {org['name']}")

print("\n" + "=" * 70)
print("Next step: Copy these rows into your Google Sheet Nodes tab")
print("=" * 70)
