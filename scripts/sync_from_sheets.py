#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas"]
# ///
"""
Sync nodes and edges from Google Sheets to CSV files.

Google Sheet: https://docs.google.com/spreadsheets/d/1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc/

Simplified approach:
- Funders are regular rows in Nodes tab with category="Funder"
- Script auto-generates funding edges based on status field
"""

import pandas as pd
import sys
from pathlib import Path

# Configuration
SPREADSHEET_ID = "1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc"
SHEET_IDS = {
    "nodes": "941366450",      # Nodes tab (includes funders)
    "edges": "562789525",      # Edges tab
}

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "processed"

def get_sheet_url(gid):
    """Generate CSV export URL for a Google Sheet tab."""
    return f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={gid}"

def load_sheet(name, gid):
    """Load a Google Sheet tab as a DataFrame."""
    url = get_sheet_url(gid)
    print(f"Loading {name} sheet (gid={gid})...")
    try:
        df = pd.read_csv(url)
        print(f"✓ Loaded {len(df)} rows from {name}")
        return df
    except Exception as e:
        print(f"✗ Failed to load {name}: {e}")
        print("\n" + "="*60)
        print("SETUP REQUIRED:")
        print("="*60)
        print("\n1. Make the Google Sheet publicly accessible:")
        print("   • Open the sheet")
        print("   • Click 'Share' (top right)")
        print("   • Change 'Restricted' to 'Anyone with the link'")
        print("   • Set permission to 'Viewer'")
        print("   • Click 'Done'")
        print(f"\n2. Current URL: {url}")
        print("\n3. Re-run this script")
        print("="*60 + "\n")
        sys.exit(1)

def generate_funding_edges(nodes_df):
    """
    Auto-generate funding edges for funders based on status.

    Rule: category="Funder" AND status="4. approved" → creates "funds" edge to PEDP
    """
    funding_edges = []

    # Find funders with approved status
    funders = nodes_df[
        (nodes_df['category'] == 'Funder') &
        (nodes_df['status'].str.contains('4', na=False) | nodes_df['status'].str.contains('approved', na=False))
    ]

    for idx, funder in funders.iterrows():
        edge = {
            'source': funder['id'],
            'target': 'PEDP',
            'relationship_type': 'funds'
        }
        funding_edges.append(edge)
        print(f"  • {funder['name']}: status '{funder['status']}' → funds PEDP")

    return pd.DataFrame(funding_edges)

def main():
    print("="*60)
    print("PEDP Network Map - Google Sheets Sync")
    print("="*60 + "\n")

    # Load nodes and edges
    nodes_df = load_sheet("Nodes", SHEET_IDS["nodes"])
    edges_df = load_sheet("Edges", SHEET_IDS["edges"])

    # Auto-generate funding edges
    print("\nGenerating funding edges for approved funders...")
    funding_edges_df = generate_funding_edges(nodes_df)

    if len(funding_edges_df) > 0:
        # Add to existing edges
        edges_df = pd.concat([edges_df, funding_edges_df], ignore_index=True)
        print(f"\n✓ Added {len(funding_edges_df)} funding edges")
    else:
        print("  (No approved funders found)")

    # Ensure required columns exist
    required_node_cols = ['id', 'name', 'organization', 'contact', 'description',
                          'status', 'website', 'category', 'timeline', 'color']
    for col in required_node_cols:
        if col not in nodes_df.columns:
            nodes_df[col] = ''

    required_edge_cols = ['source', 'target', 'relationship_type']
    for col in required_edge_cols:
        if col not in edges_df.columns:
            edges_df[col] = ''

    # Save to CSV
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    nodes_file = OUTPUT_DIR / "nodes.csv"
    edges_file = OUTPUT_DIR / "edges.csv"

    nodes_df[required_node_cols].to_csv(nodes_file, index=False)
    edges_df[required_edge_cols].to_csv(edges_file, index=False)

    print("\n" + "="*60)
    print("SYNC COMPLETE ✓")
    print("="*60)
    print(f"\n📁 Saved {len(nodes_df)} nodes to: {nodes_file}")
    print(f"📁 Saved {len(edges_df)} edges to: {edges_file}")

    # Show summary
    print("\n=== Entity Summary ===")
    print(nodes_df['category'].value_counts().to_string())

    print("\n=== Relationship Summary ===")
    print(edges_df['relationship_type'].value_counts().to_string())

    print("\nNext steps:")
    print("  1. Review the generated CSV files")
    print("  2. Run the notebook to regenerate visualization:")
    print("     jupyter nbconvert --execute --to notebook --inplace notebooks/network_visualization.ipynb")
    print("  3. Open outputs/network_map.html\n")

if __name__ == "__main__":
    main()
