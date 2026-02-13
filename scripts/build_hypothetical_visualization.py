#!/usr/bin/env python3
"""
Generate hypothetical network visualization - EXACT COPY of current network code
but with hypothetical data loaded.
"""

import networkx as nx
import pandas as pd
from pyvis.network import Network
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("PEDP Network - Hypothetical Future State Generator")
print("="*60)

# Edge styling by relationship type (EXACT SAME as current network)
EDGE_STYLES = {
    'is a member of': {'color': '#8e44ad', 'width': 2.5, 'arrows': 'to'},
    'funds': {'color': '#27ae60', 'width': 3, 'arrows': 'to'},
    'coordinates action with': {'color': '#3498db', 'width': 2, 'arrows': 'to;from'},
    'hypothetical connection': {'color': '#999999', 'width': 1.5, 'arrows': 'to', 'dashes': True}
}

# Load COMBINED data (current + hypothetical)
print("\n1. Loading data...")
nodes_current = pd.read_csv('data/processed/nodes.csv')
nodes_hyp = pd.read_csv('data/processed/nodes_hypothetical.csv')
nodes_df = pd.concat([nodes_current, nodes_hyp], ignore_index=True)

edges_current = pd.read_csv('data/processed/edges.csv')
edges_hyp = pd.read_csv('data/processed/edges_hypothetical.csv')
edges_df = pd.concat([edges_current, edges_hyp], ignore_index=True)

positions_current = pd.read_csv('data/processed/node_positions.csv')
positions_hyp = pd.read_csv('data/processed/node_positions_hypothetical.csv')
positions_df = pd.concat([positions_current, positions_hyp], ignore_index=True)

# Load color config and create mapping (EXACT SAME as current)
colors_df = pd.read_csv('data/processed/colors.csv')
color_map = dict(zip(colors_df['name'], colors_df['hex']))
nodes_df['hex_color'] = nodes_df['color'].map(color_map)

# Create positions mapping (EXACT SAME as current - use original fixed values)
positions_map = {row['id']: {'x': row['x'], 'y': row['y'], 'fixed': row['fixed']}
                 for _, row in positions_df.iterrows()}

print(f"   Nodes: {len(nodes_df)} ({len(nodes_current)} current + {len(nodes_hyp)} hypothetical)")
print(f"   Edges: {len(edges_df)} ({len(edges_current)} current + {len(edges_hyp)} hypothetical)")

# Build graph with ALL edges (current + hypothetical)
print("\n2. Building network graph...")
G = nx.DiGraph()

for _, row in nodes_df.iterrows():
    G.add_node(
        row['id'],
        name=row['name'],
        organization=row['organization'],
        category=row['category'],
        description=row['description'],
        status=row['status'],
        timeline=row['timeline']
    )

for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], relationship_type=row['relationship_type'])

G_undirected = G.to_undirected()

# Calculate centrality on REAL edges only (for node sizing)
print("\n3. Calculating centrality (on REAL edges only for sizing)...")
G_real = nx.DiGraph()
G_real.add_nodes_from(G.nodes(data=True))
for source, target, data in G.edges(data=True):
    if data['relationship_type'] != 'hypothetical connection':
        G_real.add_edge(source, target, **data)

G_real_undirected = G_real.to_undirected()

# Create filtered graph for node sizing (EXACT SAME as current)
G_filtered = nx.DiGraph()
G_filtered.add_nodes_from(G_real.nodes(data=True))
for source, target, data in G_real.edges(data=True):
    if data['relationship_type'] != 'Interested in solving the problem':
        G_filtered.add_edge(source, target, **data)

G_filtered_undirected = G_filtered.to_undirected()
degree_centrality_for_sizing = nx.degree_centrality(G_filtered_undirected)

# Create PyVis visualization (EXACT SAME settings as current)
print("\n4. Creating interactive visualization...")
net = Network(
    height='800px',
    width='100%',
    bgcolor='#f8f8f8',  # Light grey (only difference from current)
    font_color='#333333',
    directed=True
)

# EXACT SAME physics as current network
net.barnes_hut(
    gravity=-3000,
    central_gravity=0.1,
    spring_length=150,
    spring_strength=0.01,
    damping=0.2,
    overlap=0
)

# Add nodes (EXACT SAME code as current network)
for node in G.nodes():
    node_data = nodes_df[nodes_df['id'] == node].iloc[0]
    is_hypothetical = node.startswith('HYP-')

    color = node_data['hex_color']

    # SIZE STRATEGY (EXACT SAME as current)
    if node_data['category'] == 'Funder':
        size = 20
    else:
        # Only calculate for non-hypothetical nodes
        if not is_hypothetical:
            size = 15 + (degree_centrality_for_sizing.get(node, 0) * 200)
        else:
            size = 30  # Fixed size for hypothetical nodes

    # Build tooltip (EXACT SAME as current)
    tooltip_lines = [node_data['name'], f"Category: {node_data['category']}", ""]

    if is_hypothetical:
        tooltip_lines.append("⚠️ HYPOTHETICAL ORGANIZATION (NOT REAL)")
        tooltip_lines.append("")
        tooltip_lines.append(node_data['description'])
    else:
        node_degree = G_real_undirected.degree(node) if node in G_real_undirected else 0

        if node_degree == 0:
            if node_data['category'] == 'Funder':
                tooltip_lines.append("Interested in working in this space")
            else:
                tooltip_lines.append("Actively working in this space")
        else:
            connections = {
                'member_of': [], 'has_members': [],
                'funds': [], 'funded_by': [], 'coordinates': []
            }

            for _, target, edge_data in G_real.out_edges(node, data=True):
                rel_type = edge_data['relationship_type']
                target_name = G_real.nodes[target]['name']
                if rel_type == "is a member of":
                    connections['member_of'].append(target_name)
                elif rel_type == "funds":
                    connections['funds'].append(target_name)
                elif rel_type == "coordinates action with":
                    connections['coordinates'].append(target_name)

            for source, _, edge_data in G_real.in_edges(node, data=True):
                rel_type = edge_data['relationship_type']
                source_name = G_real.nodes[source]['name']
                if rel_type == "is a member of":
                    connections['has_members'].append(source_name)
                elif rel_type == "funds":
                    connections['funded_by'].append(source_name)
                elif rel_type == "coordinates action with":
                    if source_name not in connections['coordinates']:
                        connections['coordinates'].append(source_name)

            if connections['member_of']:
                tooltip_lines.append("Member of:")
                for org in sorted(connections['member_of']):
                    tooltip_lines.append(f"• {org}")
                tooltip_lines.append("")
            if connections['has_members']:
                tooltip_lines.append("Has members:")
                for org in sorted(connections['has_members']):
                    tooltip_lines.append(f"• {org}")
                tooltip_lines.append("")
            if connections['funds']:
                tooltip_lines.append("Funds:")
                for org in sorted(connections['funds']):
                    tooltip_lines.append(f"• {org}")
                tooltip_lines.append("")
            if connections['funded_by']:
                tooltip_lines.append("Funded by:")
                for org in sorted(connections['funded_by']):
                    tooltip_lines.append(f"• {org}")
                tooltip_lines.append("")
            if connections['coordinates']:
                tooltip_lines.append("Coordinates with:")
                for org in sorted(connections['coordinates']):
                    tooltip_lines.append(f"• {org}")

    title = "\n".join(tooltip_lines).rstrip()
    pos = positions_map[node]

    # Add node - different styling for hypothetical
    if is_hypothetical:
        net.add_node(
            node,
            label=f"[HYPOTHETICAL]\n{node_data['name']}",
            title=title,
            color=color,
            size=size,
            borderWidth=3,
            shape='box',
            font={'color': '#666666'},
            x=pos['x'],
            y=pos['y'],
            fixed=pos['fixed']
        )
    else:
        net.add_node(
            node,
            label=node_data['name'],
            title=title,
            color=color,
            size=size,
            borderWidth=2,
            borderWidthSelected=4,
            x=pos['x'],
            y=pos['y'],
            fixed=pos['fixed']
        )

# Add edges (EXACT SAME as current)
for edge in G.edges(data=True):
    rel_type = edge[2]['relationship_type']
    style = EDGE_STYLES[rel_type]

    edge_config = {
        'color': style['color'],
        'width': style['width'],
        'arrows': style['arrows'],
        'title': rel_type,
        'smooth': {'type': 'continuous'},
        'arrowStrikethrough': False
    }

    if style.get('dashes'):
        edge_config['dashes'] = True

    net.add_edge(edge[0], edge[1], **edge_config)

# Save
print("\n5. Saving visualization...")
net.save_graph('outputs/network_map_hypothetical.html')
print(f"   ✓ Saved to: outputs/network_map_hypothetical.html")

print("\n✅ Hypothetical visualization generated!")
print("   Uses EXACT same physics and styling as current network")
print("   Only difference: light grey background + 2 hypothetical nodes + 50 grey edges")
