# Quick Editing Guide

The network visualization is **100% CSV-driven** with separate color config - no code changes needed!

## Color System (2-File Approach)

### 1. Define Color Palette (`data/processed/colors.csv`)

```csv
name,hex
red,#e74c3c
green,#2ecc71
blue,#3498db
orange,#f39c12
purple,#9b59b6
teal,#1abc9c
```

**Add/edit colors here** - these are your color variables.

### 2. Assign Colors to Nodes (`data/processed/nodes.csv`)

```csv
id,name,...,color
PEDP,Public Environmental Data Partners,...,green
AGU,American Geophysical Union,...,red
```

**Use color variable names** (red, green, blue, etc.) - not hex codes!

### Benefits

✅ **Change global colors once** - edit `colors.csv` to update all nodes using that color
✅ **Consistent theming** - reuse color names across nodes
✅ **Easy customization** - add new color variables anytime

## Change the Color Scheme

Edit `data/processed/colors.csv`:

```csv
name,hex
red,#ff0000     ← Change this hex code
green,#00ff00   ← All nodes using "green" update automatically
```

## Assign Different Colors to Nodes

Edit `data/processed/nodes.csv`:

```csv
PEDP,...,green   ← Change from green to...
PEDP,...,purple  ← ...purple (uses hex from colors.csv)
```

## Add a New Color

1. Add to `colors.csv`:
```csv
name,hex
gold,#ffd700
```

2. Use in `nodes.csv`:
```csv
NewOrg,...,gold
```

## Add a New Node

Add a row to `data/processed/nodes.csv`:

```csv
NewOrg,New Organization Name,Parent Org,,Description here,Established,,Category,Timeline,red
```

**Use a color variable name** from `colors.csv` (e.g., `red`, `green`, `blue`)

## Add/Remove Relationships

Edit `data/processed/edges.csv`:

```csv
source,target,relationship_type
NewOrg,PEDP,is a member of
DataFoundation,NewOrg,funds
NewOrg,AGU,coordinates action with
```

**Relationship types:**
- `is a member of` - Purple arrow (member → parent)
- `funds` - Green arrow (funder → recipient)
- `coordinates action with` - Blue bidirectional (mutual)

## Regenerate Visualization

After editing CSV files:

```bash
jupyter nbconvert --execute --to notebook --inplace notebooks/network_visualization.ipynb
open outputs/network_map.html
```

Or just run all cells in Jupyter Lab.

## Current Color Scheme

| Variable | Hex | Current Use |
|----------|-----|-------------|
| `red` | `#e74c3c` | Data Coordination/Standards (7 nodes) |
| `green` | `#2ecc71` | Data Preservation/Archiving (5 nodes) |
| `blue` | `#3498db` | Data Collection/Monitoring (1 node) |
| `orange` | `#f39c12` | Capacity Building/Support (3 nodes) |
| `purple` | `#9b59b6` | Communication/Access (1 node) |
| `teal` | `#1abc9c` | Advocacy/Community Focus (1 node) |

**Edit colors.csv to change these globally!**
