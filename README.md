# PEDP Climate & Environmental Data Initiatives Network Map v2.0

Interactive network visualization of 19 climate and environmental data initiatives with typed relationships showing organizational hierarchy and funding flows.

## Overview

This project visualizes the ecosystem of climate and environmental data initiatives described in the "2025 11 18 Emerging Climate and Environmental Data Initiatives; Read-Ahead Funder Briefing" document. The interactive map enables quick exploration of how these initiatives connect and identifies central hubs in the coordination network.

## Updates in v2.0

- **19 nodes** (added 3 PEDP members: OEDP, EPIC, EDGI)
- **3 relationship types** with directional arrows:
  - 🟣 Purple: "is a member of" (member → parent org)
  - 🟢 Green: "funds" (funder → recipient)
  - 🔵 Blue: "coordinates action with" (bidirectional)
- **Thicker edges** (2-3px) for better visibility
- **Directed graph** showing organizational hierarchy and funding flows

**Key Features:**
- 🎨 Color-coded nodes by initiative category
- 📊 Node size proportional to degree centrality (number of connections)
- 🔍 Rich hover tooltips with organization details
- 📈 Centrality metrics to identify key hubs (PEDP, Data Foundation, NASEM)
- 🎯 Force-directed layout for intuitive clustering
- 🖱️ Interactive: drag, zoom, pan, and explore
- ➡️ Directional arrows showing relationship types

## Quick Start

### Prerequisites

- **Python 3.12+** (required)
- **uv** - Python environment manager ([install instructions](https://github.com/astral-sh/uv))

### Installation

```bash
# Navigate to project directory
cd PEDP-Network-Map

# Create virtual environment with uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install networkx pyvis pandas jupyter jupyterlab

# Launch Jupyter Lab
jupyter lab
```

**Alternative (using uv run):**
```bash
cd PEDP-Network-Map
uv venv
uv run --with jupyter --with networkx --with pyvis --with pandas jupyter lab
```

### Usage

1. Open `notebooks/network_visualization.ipynb` in Jupyter Lab
2. Run all cells: **Cell → Run All** (or Shift+Enter through each cell)
3. The notebook will:
   - Load the 19 initiatives and their relationships (membership, funding, coordination)
   - Build the directed network graph
   - Calculate centrality metrics
   - Generate an interactive HTML visualization with styled edges
4. Open `outputs/network_map.html` in your browser to explore the network

## 🔮 Hypothetical Future Network

**NEW**: In addition to the current network visualization, this project includes a **hypothetical future state** visualization showing how the isolated organizations could become connected through strategic intermediary hubs.

### What is it?

The hypothetical network shows a scenario analysis where:
- **2 new intermediary organizations** (Regional Data Coordination Hub, Funder Collaborative Network) connect the ecosystem
- **46 isolated organizations** become engaged through these hubs
- The network transforms from **47 disconnected components** to **1 fully connected network**

### Key Differences

| Aspect | Current Network | Hypothetical Network |
|--------|----------------|---------------------|
| **Nodes** | 78 organizations | 80 (78 + 2 intermediaries) |
| **Edges** | 55 relationships | 105 (55 + 50 hypothetical) |
| **Components** | 47 disconnected | 1 fully connected |
| **Isolated** | 46 organizations | 0 organizations |

### Visual Indicators

⚠️ The hypothetical visualization includes multiple warnings to prevent confusion:
- Purple banner: "HYPOTHETICAL FUTURE STATE - NOT CURRENT NETWORK"
- Watermark: "SCENARIO ANALYSIS" across the page
- Light grey background (vs white for current)
- Grey dashed edges for hypothetical connections
- Box-shaped nodes for intermediaries
- [HYPOTHETICAL] labels on new nodes

### Building Both Visualizations

```bash
# Build both current and hypothetical networks
./scripts/build_visualizations.sh
```

This generates:
- `outputs/network_map.html` - Current network
- `outputs/network_map_hypothetical.html` - Hypothetical future state

Open both side-by-side in your browser to compare!

### Use Cases

- **Strategic Planning**: Identify what types of intermediary organizations would connect the ecosystem
- **Investment Justification**: Show before/after impact of coordination hubs
- **Partnership Development**: Visualize pathways to engage isolated funders and practitioners
- **Stakeholder Communication**: Demonstrate the fragmentation problem and potential solutions

📖 **Full Documentation**: See [HYPOTHETICAL_NETWORK.md](HYPOTHETICAL_NETWORK.md) for complete details on how to modify, build, and use the hypothetical network.

## Project Structure

```
PEDP-Network-Map/
├── README.md                           # This file
├── pyproject.toml                      # Python dependencies
├── verify_setup.py                     # Setup verification script
├── .gitignore                          # Git ignore rules
├── data/
│   └── processed/
│       ├── nodes.csv                   # 19 initiatives with metadata + color variables
│       ├── edges.csv                   # 42 typed relationships
│       └── colors.csv                  # Color palette config (variable → hex)
├── notebooks/
│   └── network_visualization.ipynb     # Main analysis notebook
└── outputs/
    └── network_map.html                # Generated interactive visualization
```

## Data Schema

### Nodes (19 initiatives)

**CSV-Driven:** All node properties are defined in `nodes.csv` for easy editing.

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (short code) |
| `name` | Full initiative name |
| `organization` | Parent organization |
| `contact` | Contact information (if available) |
| `description` | Brief description of the initiative |
| `status` | Current status (Established/Emerging/Recently Launched) |
| `website` | Website URL (if available) |
| `category` | Primary category (see categories below) |
| `timeline` | Timeline classification |
| `color` | **Color variable name** (maps to hex in `colors.csv`) |

### Colors Config

**Separate color palette** defined in `colors.csv`:

| Variable | Hex | Usage |
|----------|-----|-------|
| `red` | `#e74c3c` | Data Coordination/Standards |
| `green` | `#2ecc71` | Data Preservation/Archiving |
| `blue` | `#3498db` | Data Collection/Monitoring |
| `orange` | `#f39c12` | Capacity Building/Support |
| `purple` | `#9b59b6` | Communication/Access |
| `teal` | `#1abc9c` | Advocacy/Community Focus |

**Benefits:** Change a hex code once in `colors.csv` to update all nodes using that color variable.

**Categories:**
- Data Collection/Monitoring
- Data Preservation/Archiving
- Data Coordination/Standards
- Capacity Building/Support
- Communication/Access
- Advocacy/Community Focus

### Edges (42 relationships)

**CSV-Driven:** All relationships are defined in `edges.csv` for easy editing.

| Relationship Type | Direction | Count | Description |
|------------------|-----------|-------|-------------|
| `is a member of` | Directional | 4 | Member organization → parent org (e.g., ImpactProject → PEDP) |
| `funds` | Directional | 5 | Funding organization → recipient (e.g., DataFoundation → Cornerstone) |
| `coordinates action with` | Bidirectional | 33 | Mutual coordination and collaboration (rendered with bidirectional arrows) |

**Note:** PEDP members have only membership edges to PEDP (no redundant coordination edges).

## Network Statistics

**Source of Truth:** All data comes from CSV files in `data/processed/`

Based on the current data:

- **Nodes:** 19 initiatives
- **Edges:** 42 typed relationships
- **Graph Type:** Directed (with bidirectional coordination edges)
- **Network Density:** ~0.24 (24% of possible connections exist)
- **Top Hubs:** PEDP, Data Foundation, NASEM
- **PEDP Members:** 4 (ImpactProject, OEDP, EPIC, EDGI)
- **Funded Initiatives:** 5 (Cornerstone, GRQD, CDAN, KCF, ImpactProject)

## Visualization Guide

**Interacting with the Map:**
- **Drag nodes** to reposition them manually
- **Hover** over nodes to see detailed information tooltips
- **Hover over edges** to see relationship type
- **Zoom** with mouse wheel or trackpad gestures
- **Pan** by clicking and dragging on empty space
- **Toggle physics** (⚙️ button) to freeze/unfreeze the layout

**Visual Encoding:**
- **Node color** = Category (6 distinct colors)
- **Node size** = Degree centrality (larger = more connections)
- **Edge color & arrows** = Relationship type:
  - 🟣 Purple arrows: "is a member of" (member → parent org)
  - 🟢 Green arrows: "funds" (funder → recipient)
  - 🔵 Blue bidirectional: "coordinates action with" (mutual)

## Centrality Metrics Explained

The notebook calculates three types of centrality:

1. **Degree Centrality**: Number of direct connections
   - Identifies the most connected "hubs"
   - Example: PEDP has 10 connections

2. **Betweenness Centrality**: How often a node lies on shortest paths
   - Identifies "bridge" nodes connecting different clusters
   - High betweenness = important for information flow

3. **Closeness Centrality**: Average distance to all other nodes
   - Identifies nodes that can spread information quickly
   - High closeness = central position in network

## Editing the Network

**Google Sheets Integration:** Auto-sync from Google Sheets (recommended) or edit CSV files directly.

### Option 1: Google Sheets (Recommended)

Edit your Google Sheet, then sync:
```bash
./scripts/sync_from_sheets.py
```

Uses `uv` to automatically install dependencies - no manual setup needed!

**Setup:** See `SHEETS_SETUP.md` for one-time configuration.

**Funder List Processing:** Automatically adds funders with appropriate edges based on status.

### Option 2: Direct CSV Editing

**CSV Files = Source of Truth:** All network data is stored in CSV files for easy editing.

### Changing Colors

**Global color change** - Edit `data/processed/colors.csv`:
```csv
name,hex
green,#00ff00  ← All nodes using "green" update automatically
```

**Per-node color change** - Edit `data/processed/nodes.csv`:
```csv
PEDP,Public Environmental Data Partners,...,green
PEDP,Public Environmental Data Partners,...,purple  ← Change color variable
```

### Adding New Initiatives

1. Add a row to `data/processed/nodes.csv` with all required fields including `color`
2. Add relationships to `data/processed/edges.csv` with appropriate `relationship_type`
3. Re-run the notebook to regenerate the visualization

### Modifying Relationships

Edit `data/processed/edges.csv` directly:
- Add/remove rows to change network connections
- Change `relationship_type` to one of: `is a member of`, `funds`, `coordinates action with`
- Coordination edges are bidirectional (only need one direction in CSV)

### Modifying Visualization

Key parameters in the notebook:

```python
# Node colors by category
NODE_COLORS = {
    'Data Collection/Monitoring': '#3498db',
    'Data Preservation/Archiving': '#2ecc71',
    # ... etc
}

# Physics simulation parameters
net.barnes_hut(
    gravity=-8000,          # Node repulsion
    central_gravity=0.3,    # Pull toward center
    spring_length=200,      # Edge length
    spring_strength=0.001,  # Edge stiffness
)

# Node size scaling
size = 15 + (degree_centrality[node] * 200)
```

## Technologies Used

- **NetworkX** (3.2+): Graph analysis and algorithms
- **PyVis** (0.3.2+): Interactive network visualization
- **Pandas** (2.1.0+): Data manipulation
- **Jupyter** (1.0.0+): Interactive notebook environment

## License

This project analyzes publicly available information about climate and environmental data initiatives for research and coordination purposes.

## Contact

For questions about the PEDP network or this visualization, please contact the Public Environmental Data Partners (PEDP).

---

**Generated:** February 2026
**Source:** 2025 11 18 Emerging Climate and Environmental Data Initiatives; Read-Ahead Funder Briefing
