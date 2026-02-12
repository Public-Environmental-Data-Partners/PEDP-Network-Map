#!/usr/bin/env python3
"""Quick verification script to test the network data and dependencies."""

import sys

def verify_imports():
    """Verify all required packages are installed."""
    print("Checking imports...")
    try:
        import networkx as nx
        import pandas as pd
        from pyvis.network import Network
        print(f"✓ NetworkX {nx.__version__}")
        print(f"✓ Pandas {pd.__version__}")
        print("✓ PyVis imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def verify_data():
    """Verify data files load correctly."""
    print("\nChecking data files...")
    try:
        import pandas as pd

        nodes_df = pd.read_csv('data/processed/nodes.csv')
        edges_df = pd.read_csv('data/processed/edges.csv')

        print(f"✓ Loaded {len(nodes_df)} nodes")
        print(f"✓ Loaded {len(edges_df)} edges")

        # Verify expected structure
        assert len(nodes_df) == 19, f"Expected 19 nodes, got {len(nodes_df)}"
        assert len(edges_df) >= 40, f"Expected 40+ edges, got {len(edges_df)}"
        assert 'id' in nodes_df.columns, "Missing 'id' column in nodes"
        assert 'color' in nodes_df.columns, "Missing 'color' column in nodes"
        assert 'source' in edges_df.columns, "Missing 'source' column in edges"
        assert 'relationship_type' in edges_df.columns, "Missing 'relationship_type' column in edges"

        # Check relationship types exist
        rel_types = set(edges_df['relationship_type'].unique())
        expected_types = {'is a member of', 'funds', 'coordinates action with'}
        assert rel_types == expected_types, f"Missing types: {expected_types - rel_types}"

        # Verify PEDP membership
        membership = edges_df[edges_df['relationship_type'] == 'is a member of']
        assert len(membership) >= 4, f"Expected 4+ PEDP members, got {len(membership)}"
        assert all(membership['target'] == 'PEDP'), "All membership should point to PEDP"

        print("✓ Data structure verified")
        print(f"✓ Found {len(membership)} PEDP members")
        print(f"✓ Relationship types: {', '.join(rel_types)}")
        return True
    except Exception as e:
        print(f"✗ Data error: {e}")
        return False

def verify_network():
    """Verify network can be built."""
    print("\nBuilding network...")
    try:
        import networkx as nx
        import pandas as pd

        nodes_df = pd.read_csv('data/processed/nodes.csv')
        edges_df = pd.read_csv('data/processed/edges.csv')

        G = nx.DiGraph()

        for idx, row in nodes_df.iterrows():
            G.add_node(row['id'], name=row['name'])

        for idx, row in edges_df.iterrows():
            G.add_edge(row['source'], row['target'], relationship_type=row['relationship_type'])

        print(f"✓ Network built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        print(f"✓ Graph type: {'Directed' if nx.is_directed(G) else 'Undirected'}")

        # Convert to undirected for connectivity check
        G_undirected = G.to_undirected()
        print(f"✓ Network density: {nx.density(G_undirected):.3f}")
        print(f"✓ Network connected: {nx.is_connected(G_undirected)}")

        # Calculate centrality on undirected version
        degree_centrality = nx.degree_centrality(G_undirected)
        top_node = max(degree_centrality.items(), key=lambda x: x[1])
        top_name = nodes_df[nodes_df['id'] == top_node[0]]['name'].values[0]

        print(f"✓ Most connected: {top_name} ({G_undirected.degree(top_node[0])} connections)")

        return True
    except Exception as e:
        print(f"✗ Network error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification checks."""
    print("="*60)
    print("PEDP Network Map - Setup Verification")
    print("="*60)

    checks = [
        ("Dependencies", verify_imports),
        ("Data Files", verify_data),
        ("Network Build", verify_network),
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))

    print("\n" + "="*60)
    print("Summary:")
    print("="*60)

    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20s} {status}")
        if not result:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n🎉 All checks passed! You're ready to run the notebook.")
        print("\nNext steps:")
        print("  1. jupyter lab")
        print("  2. Open notebooks/network_visualization.ipynb")
        print("  3. Run all cells")
        return 0
    else:
        print("\n❌ Some checks failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
