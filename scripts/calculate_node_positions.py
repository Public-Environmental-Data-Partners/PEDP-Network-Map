#!/usr/bin/env python3
"""
Calculate spatial positions for network nodes based on connection status and category.

Creates a CSV file with initial x,y positions for each node:
- Isolated funders → Bottom right corner
- Isolated non-funders → Top left corner
- Connected nodes → Center (with slight category bias)
"""

import pandas as pd
import sys
from pathlib import Path

# File paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
NODES_FILE = PROJECT_DIR / 'data' / 'processed' / 'nodes.csv'
EDGES_FILE = PROJECT_DIR / 'data' / 'processed' / 'edges.csv'
OUTPUT_FILE = PROJECT_DIR / 'data' / 'processed' / 'node_positions.csv'


def main():
    """Calculate and output node positions."""

    # Load data
    print("Loading nodes and edges...")
    nodes_df = pd.read_csv(NODES_FILE)
    edges_df = pd.read_csv(EDGES_FILE)

    print(f"Loaded {len(nodes_df)} nodes and {len(edges_df)} edges")

    # Identify connected nodes (any node that appears in edges)
    connected_nodes = set(edges_df['source'].tolist() + edges_df['target'].tolist())
    print(f"Found {len(connected_nodes)} connected nodes")

    # Categorize all nodes
    all_funders = nodes_df[nodes_df['category'] == 'Funder']['id'].tolist()
    isolated_funders = [f for f in all_funders if f not in connected_nodes]
    isolated_non_funders = [
        n for n in nodes_df['id']
        if n not in connected_nodes and n not in all_funders
    ]
    connected_funders = [f for f in all_funders if f in connected_nodes]
    connected_non_funders = [
        n for n in nodes_df['id']
        if n in connected_nodes and n not in all_funders
    ]

    print(f"\nNode distribution:")
    print(f"  Connected funders: {len(connected_funders)}")
    print(f"  Connected non-funders: {len(connected_non_funders)}")
    print(f"  Isolated funders: {len(isolated_funders)}")
    print(f"  Isolated non-funders: {len(isolated_non_funders)}")

    # COORDINATE SYSTEM: PyVis uses pixel coordinates
    # Canvas size: 800px height × variable width (assume ~1200px)
    # Origin: Center (0, 0) with x: [-600, 600], y: [-400, 400]

    positions = []

    # 1. ISOLATED FUNDERS → Bottom Right (x: 400-600, y: 200-400)
    print(f"\nPositioning {len(isolated_funders)} isolated funders in bottom right...")
    for i, node_id in enumerate(isolated_funders):
        # Cluster with slight spacing to avoid perfect overlap
        x = 450 + (i % 5) * 30  # 5 columns, 30px spacing
        y = 250 + (i // 5) * 30  # Rows of 5, 30px spacing
        positions.append({
            'id': node_id,
            'x': x,
            'y': y,
            'fixed': False  # Allow some movement but gravity pulls them back
        })

    # 2. ISOLATED NON-FUNDERS → Top Left (x: -600 to -400, y: -400 to -200)
    print(f"Positioning {len(isolated_non_funders)} isolated non-funders in top left...")
    for i, node_id in enumerate(isolated_non_funders):
        x = -500 - (i % 5) * 30
        y = -300 - (i // 5) * 30
        positions.append({
            'id': node_id,
            'x': x,
            'y': y,
            'fixed': False
        })

    # 3. CONNECTED FUNDERS → Center with slight bias toward bottom right
    print(f"Positioning {len(connected_funders)} connected funders in center-right...")
    for node_id in connected_funders:
        positions.append({
            'id': node_id,
            'x': 75,   # Center-right
            'y': 50,   # Center-bottom
            'fixed': False  # Let physics adjust based on edges
        })

    # 4. CONNECTED NON-FUNDERS → Center with slight bias toward top left
    print(f"Positioning {len(connected_non_funders)} connected non-funders in center-left...")
    for node_id in connected_non_funders:
        positions.append({
            'id': node_id,
            'x': -75,  # Center-left
            'y': -50,  # Center-top
            'fixed': False
        })

    # Create DataFrame and save
    positions_df = pd.DataFrame(positions)
    positions_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Saved {len(positions_df)} node positions to: {OUTPUT_FILE}")
    print(f"\nSummary:")
    print(f"  - {len(isolated_funders)} isolated funders (bottom right)")
    print(f"  - {len(isolated_non_funders)} isolated non-funders (top left)")
    print(f"  - {len(connected_funders) + len(connected_non_funders)} connected nodes (center)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
