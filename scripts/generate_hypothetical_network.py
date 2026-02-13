#!/usr/bin/env python3
"""
Generate hypothetical network data for future state visualization.

Creates:
- nodes_hypothetical.csv: 2 new intermediary nodes
- edges_hypothetical.csv: ~50 hypothetical connections
- node_positions_hypothetical.csv: Positions for new nodes
"""

import pandas as pd
import networkx as nx

# Load current data
print("Loading current network data...")
nodes_df = pd.read_csv('data/processed/nodes.csv')
edges_df = pd.read_csv('data/processed/edges.csv')
positions_df = pd.read_csv('data/processed/node_positions.csv')

# Build current network graph to identify isolated nodes
print("Building network graph...")
G = nx.DiGraph()
G.add_nodes_from(nodes_df['id'])
for _, edge in edges_df.iterrows():
    G.add_edge(edge['source'], edge['target'])

# Convert to undirected to check connectivity
G_undirected = G.to_undirected()

# Identify isolated nodes (degree = 0)
isolated_nodes = [node for node in G.nodes() if G_undirected.degree(node) == 0]
print(f"Found {len(isolated_nodes)} isolated nodes")

# Split isolated nodes into funders and non-funders
isolated_funders = []
isolated_nonfunders = []

for node_id in isolated_nodes:
    node_data = nodes_df[nodes_df['id'] == node_id].iloc[0]
    if node_data['category'] == 'Funder':
        isolated_funders.append(node_id)
    else:
        isolated_nonfunders.append(node_id)

print(f"  - {len(isolated_funders)} isolated funders")
print(f"  - {len(isolated_nonfunders)} isolated non-funders")

# Create 2 new hypothetical intermediary nodes
print("\nCreating hypothetical intermediary nodes...")
hypothetical_nodes = pd.DataFrame([
    {
        'id': 'HYP-HUB1',
        'name': 'Regional Data Coordination Hub',
        'organization': 'Regional Data Coordination Hub',
        'contact': '',
        'description': '[HYPOTHETICAL] Regional organization coordinating data initiatives and connecting funders with practitioners',
        'status': 'Hypothetical',
        'website': '',
        'category': 'Data Coordination/Standards',
        'timeline': 'Emerging/Planned',
        'color': 'red'
    },
    {
        'id': 'HYP-HUB2',
        'name': 'Funder Collaborative Network',
        'organization': 'Funder Collaborative Network',
        'contact': '',
        'description': '[HYPOTHETICAL] Funder collaborative pooling resources and coordinating grants in the environmental data space',
        'status': 'Hypothetical',
        'website': '',
        'category': 'Funder',
        'timeline': 'Emerging/Planned',
        'color': 'teal'
    }
])

# Save hypothetical nodes
hypothetical_nodes.to_csv('data/processed/nodes_hypothetical.csv', index=False)
print(f"✓ Saved {len(hypothetical_nodes)} hypothetical nodes to data/processed/nodes_hypothetical.csv")

# Create hypothetical positions for new nodes
# Position to spread out the network and reduce crowding
print("\nCreating positions for hypothetical nodes...")
hypothetical_positions = pd.DataFrame([
    {
        'id': 'HYP-HUB1',
        'x': -120,  # Top-left (toward isolated non-funders)
        'y': -120,
        'fixed': True
    },
    {
        'id': 'HYP-HUB2',
        'x': 120,   # Bottom-right (toward isolated funders)
        'y': 120,
        'fixed': True
    }
])

# Save hypothetical positions
hypothetical_positions.to_csv('data/processed/node_positions_hypothetical.csv', index=False)
print(f"✓ Saved {len(hypothetical_positions)} hypothetical positions to data/processed/node_positions_hypothetical.csv")

# Generate hypothetical edges
print("\nGenerating hypothetical edges...")
hypothetical_edges = []

# Phase 1: Connect isolated funders → HYP-HUB2
print(f"  Phase 1: Connecting {len(isolated_funders)} funders to HYP-HUB2...")
for funder_id in isolated_funders:
    hypothetical_edges.append({
        'source': funder_id,
        'target': 'HYP-HUB2',
        'relationship_type': 'hypothetical connection'
    })

# Phase 2: Connect HYP-HUB2 → Network core (PEDP, DataFoundation)
print("  Phase 2: Connecting HYP-HUB2 to network core...")
hypothetical_edges.append({
    'source': 'HYP-HUB2',
    'target': 'PEDP',
    'relationship_type': 'hypothetical connection'
})
hypothetical_edges.append({
    'source': 'HYP-HUB2',
    'target': 'DataFoundation',
    'relationship_type': 'hypothetical connection'
})

# Phase 3: Connect Network core → HYP-HUB1
print("  Phase 3: Connecting network core to HYP-HUB1...")
hypothetical_edges.append({
    'source': 'PEDP',
    'target': 'HYP-HUB1',
    'relationship_type': 'hypothetical connection'
})
hypothetical_edges.append({
    'source': 'DataFoundation',
    'target': 'HYP-HUB1',
    'relationship_type': 'hypothetical connection'
})

# Phase 4: Connect HYP-HUB1 → isolated non-funders
print(f"  Phase 4: Connecting HYP-HUB1 to {len(isolated_nonfunders)} non-funders...")
for nonfunder_id in isolated_nonfunders:
    hypothetical_edges.append({
        'source': 'HYP-HUB1',
        'target': nonfunder_id,
        'relationship_type': 'hypothetical connection'
    })

# Convert to DataFrame and save
hypothetical_edges_df = pd.DataFrame(hypothetical_edges)
hypothetical_edges_df.to_csv('data/processed/edges_hypothetical.csv', index=False)
print(f"✓ Saved {len(hypothetical_edges)} hypothetical edges to data/processed/edges_hypothetical.csv")

# Summary
print("\n" + "="*60)
print("HYPOTHETICAL NETWORK GENERATION COMPLETE")
print("="*60)
print(f"Nodes added: {len(hypothetical_nodes)}")
# Get actual positions from DataFrame
hub1_pos = hypothetical_positions[hypothetical_positions['id'] == 'HYP-HUB1'].iloc[0]
hub2_pos = hypothetical_positions[hypothetical_positions['id'] == 'HYP-HUB2'].iloc[0]
print(f"  - HYP-HUB1: Regional Data Coordination Hub (x={hub1_pos['x']}, y={hub1_pos['y']})")
print(f"  - HYP-HUB2: Funder Collaborative Network (x={hub2_pos['x']}, y={hub2_pos['y']})")
print(f"\nEdges added: {len(hypothetical_edges)}")
print(f"  - Funders → HYP-HUB2: {len(isolated_funders)}")
print(f"  - HYP-HUB2 → Core: 2")
print(f"  - Core → HYP-HUB1: 2")
print(f"  - HYP-HUB1 → Non-funders: {len(isolated_nonfunders)}")
print(f"\nFiles created:")
print(f"  - data/processed/nodes_hypothetical.csv")
print(f"  - data/processed/edges_hypothetical.csv")
print(f"  - data/processed/node_positions_hypothetical.csv")
print("="*60)
