# Hypothetical Future Network Visualization

## Overview

The hypothetical network visualization shows a **scenario analysis** of what the PEDP ecosystem could look like if isolated organizations become connected through strategic intermediary hubs.

⚠️ **IMPORTANT**: This is NOT the current network - it's a planning tool for exploring potential future states.

## What's Different from Current Network?

### Current Network (`network_map.html`)
- **78 nodes** (current organizations)
- **55 edges** (actual relationships)
- **47 disconnected components** - highly fragmented
- **46 isolated nodes** (23 funders, 23 non-funders)

### Hypothetical Network (`network_map_hypothetical.html`)
- **80 nodes** (78 current + 2 hypothetical intermediaries)
- **105 edges** (55 current + 50 hypothetical connections)
- **1 connected component** - fully connected network
- **0 isolated nodes** - everyone engaged

## Hypothetical Elements (NOT REAL)

### 1. Regional Data Coordination Hub (HYP-HUB1)
- **Position**: Between network core and isolated non-funders (top-left region)
- **Category**: Data Coordination/Standards
- **Purpose**: Coordinate data initiatives and connect practitioners
- **Connections**:
  - Receives coordination from PEDP and Data Foundation
  - Coordinates with 23 isolated non-funder organizations

### 2. Funder Collaborative Network (HYP-HUB2)
- **Position**: Between network core and isolated funders (bottom-right region)
- **Category**: Funder
- **Purpose**: Pool funder resources and coordinate grants
- **Connections**:
  - Receives interest from 23 isolated funders
  - Coordinates with PEDP and Data Foundation

## Visual Indicators

The hypothetical visualization includes multiple indicators to prevent confusion:

1. **Warning Banner** (top of page): Purple gradient banner stating "HYPOTHETICAL FUTURE STATE"
2. **Watermark**: Large semi-transparent "SCENARIO ANALYSIS" text across the visualization
3. **Light Grey Background**: Unlike the white background of the current network
4. **Page Title**: Explicitly states "Hypothetical Future State (Scenario Analysis)"
5. **Grey Edges**: All hypothetical connections are grey and dashed
6. **Box-Shaped Nodes**: Intermediary nodes are boxes (not circles)
7. **[HYPOTHETICAL] Labels**: Intermediary nodes have this prefix in their labels
8. **Legend**: Shows difference between current and hypothetical edges

## How Connections Flow

```
Isolated Funders (23)
       ↓
HYP-HUB2 (Funder Collaborative)
       ↓
PEDP ←→ Data Foundation (Network Core)
       ↓
HYP-HUB1 (Data Coordination Hub)
       ↓
Isolated Non-Funders (23)
```

All hypothetical edges are grey arrows showing this flow.

## What's Preserved from Current Network?

✅ **All 78 existing nodes in exact same positions**
- Node positions from `node_positions.csv` are preserved exactly
- All nodes are set to `fixed=True` to prevent layout shifts

✅ **All 55 existing edges unchanged**
- Purple arrows: "is a member of" (4 edges)
- Green arrows: "funds" (18 edges)
- Blue bidirectional: "coordinates action with" (33 edges)

✅ **Node sizes based on REAL connections only**
- Centrality calculations use only the 55 real edges
- PEDP remains the largest node (27 real connections)
- Hypothetical edges do not affect node sizing

## Use Cases

### 1. Strategic Planning
- **Question**: "What intermediary organizations could connect our ecosystem?"
- **Action**: Identify which types of organizations would serve as effective bridges

### 2. Investment Justification
- **Question**: "What impact would new coordination hubs have?"
- **Action**: Show before/after comparison (47 components → 1 component)

### 3. Partnership Development
- **Question**: "Where should PEDP focus partnership efforts?"
- **Action**: Visualize pathways to engage isolated funders and practitioners

### 4. Stakeholder Communication
- **Question**: "How can we explain the fragmentation problem?"
- **Action**: Open both visualizations side-by-side to show the gap

## Building the Visualizations

### Quick Build (Both Current + Hypothetical)
```bash
./scripts/build_visualizations.sh
```

This runs:
1. `generate_hypothetical_network.py` - Creates hypothetical data files
2. `jupyter nbconvert` - Builds current network
3. `build_hypothetical_visualization.py` - Builds hypothetical network
4. `add_hypothetical_watermark.py` - Adds visual indicators

### Manual Build (Hypothetical Only)
```bash
# 1. Generate hypothetical data (if not already done)
python3 scripts/generate_hypothetical_network.py

# 2. Build visualization
python3 scripts/build_hypothetical_visualization.py

# 3. Add visual indicators
python3 scripts/add_hypothetical_watermark.py
```

## Modifying the Hypothetical Network

### Add More Intermediary Nodes

Edit `scripts/generate_hypothetical_network.py`:

```python
# Add to hypothetical_nodes DataFrame
{
    'id': 'HYP-HUB3',
    'name': 'New Hub Name',
    'organization': 'New Hub Name',
    'contact': '',
    'description': '[HYPOTHETICAL] Description here',
    'status': 'Hypothetical',
    'website': '',
    'category': 'Appropriate Category',
    'timeline': 'Emerging/Planned',
    'color': 'appropriate_color'
}
```

Add position in `hypothetical_positions`:

```python
{
    'id': 'HYP-HUB3',
    'x': 100,  # x coordinate
    'y': -100, # y coordinate
    'fixed': True
}
```

Add connections in `hypothetical_edges`:

```python
hypothetical_edges.append({
    'source': 'SOURCE_NODE_ID',
    'target': 'HYP-HUB3',
    'relationship_type': 'hypothetical connection'
})
```

### Change Intermediary Positions

Edit `scripts/generate_hypothetical_network.py`:

```python
hypothetical_positions = pd.DataFrame([
    {
        'id': 'HYP-HUB1',
        'x': -200,  # Change these coordinates
        'y': -150,
        'fixed': True
    },
    # ...
])
```

### Modify Connection Strategy

Current strategy connects:
- ALL isolated funders → HYP-HUB2
- ALL isolated non-funders ← HYP-HUB1

To connect only a subset, modify `generate_hypothetical_network.py`:

```python
# Connect only first 10 funders
for funder_id in isolated_funders[:10]:
    hypothetical_edges.append({...})
```

## File Structure

```
PEDP-Network-Map/
├── data/processed/
│   ├── nodes.csv                          # 78 current nodes
│   ├── edges.csv                          # 55 current edges
│   ├── node_positions.csv                 # Positions for current nodes
│   ├── nodes_hypothetical.csv             # 2 hypothetical intermediaries
│   ├── edges_hypothetical.csv             # 50 hypothetical connections
│   └── node_positions_hypothetical.csv    # Positions for intermediaries
├── scripts/
│   ├── generate_hypothetical_network.py   # Generate hypothetical data
│   ├── build_hypothetical_visualization.py # Build visualization
│   ├── add_hypothetical_watermark.py      # Add visual indicators
│   └── build_visualizations.sh            # Build both networks
├── notebooks/
│   ├── network_visualization.ipynb        # Current network (Jupyter)
│   └── network_visualization_hypothetical.ipynb # Hypothetical (Jupyter)
├── outputs/
│   ├── network_map.html                   # Current network
│   └── network_map_hypothetical.html      # Hypothetical network
└── HYPOTHETICAL_NETWORK.md                # This file
```

## Validation

The build process includes validation to ensure:

✅ All existing node positions are preserved exactly
✅ Node sizes calculated from real edges only (not hypothetical)
✅ All 55 real edges remain unchanged
✅ Hypothetical elements clearly marked

Check validation output:

```bash
python3 scripts/build_hypothetical_visualization.py
```

Look for:
```
PEDP centrality: 27 connections (real)
PEDP centrality: 29 connections (with hypothetical)
```

This confirms PEDP's size is based on 27 real connections, not 29 total.

## Troubleshooting

### Issue: Hypothetical HTML not generated

**Solution**:
```bash
# Check if data files exist
ls -la data/processed/*hypothetical*.csv

# If missing, regenerate
python3 scripts/generate_hypothetical_network.py

# Then rebuild
python3 scripts/build_hypothetical_visualization.py
```

### Issue: Visual indicators missing

**Solution**:
```bash
# Run watermark script separately
python3 scripts/add_hypothetical_watermark.py
```

### Issue: Nodes moved from original positions

**Check**: Verify physics settings in `build_hypothetical_visualization.py`:
```python
net.barnes_hut(
    gravity=-500,           # Should be MUCH weaker than current (-3000)
    central_gravity=0.01,   # Should be near zero
    spring_strength=0.001,  # Should be weak
    damping=0.9,            # Should be high
)
```

**And verify**: All nodes have `fixed=True` in the `add_node()` calls.

## Future Enhancements

Potential additions (not yet implemented):

1. **Multiple Scenarios**: Generate A/B/C scenarios with different intermediary models
2. **Interactive Toggle**: Single HTML with button to switch between current/hypothetical
3. **Animated Transition**: Video showing current → hypothetical transformation
4. **Cost Modeling**: Tooltips showing estimated investment for each connection
5. **Phased Rollout**: Color-code edges by Year 1 / Year 2 / Year 3 implementation

## Questions?

For questions about:
- **Current network data**: See `README.md`
- **Hypothetical design decisions**: See plan document in project history
- **Technical implementation**: Review source code in `scripts/` directory
- **Modifying visualizations**: See "Modifying the Hypothetical Network" section above
