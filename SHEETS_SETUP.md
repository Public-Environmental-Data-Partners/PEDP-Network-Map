# Google Sheets Sync Setup

## Quick Setup (2 steps)

### 1. Make Sheet Publicly Readable

**Open your Google Sheet:**
https://docs.google.com/spreadsheets/d/1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc/

**Make it public:**
1. Click **Share** button (top right)
2. Change from "Restricted" to **"Anyone with the link"**
3. Set permission to **"Viewer"**
4. Click **Done**

### 2. Find Sheet IDs (gid values)

Each tab in your spreadsheet has a unique ID called a `gid`.

**To find them:**
1. Click on each tab at the bottom of the sheet
2. Look at the URL in your browser
3. Find the `gid=XXXXXXX` number

**Example:**
```
Nodes tab:       ...#gid=941366450  → gid is 941366450
Edges tab:       ...#gid=0          → gid is 0
Funder List tab: ...#gid=1234567890 → gid is 1234567890
```

**Update the script** with your gid values:

Edit `scripts/sync_from_sheets.py` and update:
```python
SHEET_IDS = {
    "nodes": "941366450",      # ← Your Nodes tab gid
    "edges": "0",              # ← Your Edges tab gid
    "funders": "1234567890"    # ← Your Funder List tab gid
}
```

## Run the Sync

After setup, run:

```bash
./scripts/sync_from_sheets.py
```

**Note:** Uses `uv` to automatically install pandas locally - no manual setup needed!

This will:
- Download data from all three tabs
- Process the Funder List according to your rules
- Generate `data/processed/nodes.csv` and `edges.csv`

## Funder List Processing Rules

The script will process funders based on their status:

| Status | Node Created? | Edge to PEDP? |
|--------|--------------|---------------|
| 0. On our radar | ✓ | ✗ |
| 1. In conversation | ✓ | ✗ |
| 2. Proposal submitted | ✓ | ✗ |
| 4. approved | ✓ | ✓ |

**All funders:**
- Get `color: teal`
- Get `category: Funding/Support`
- Indicate interest in this problem space

## Workflow

1. **Edit the Google Sheet** (add/remove nodes, edges, funders)
2. **Run sync script:** `./scripts/sync_from_sheets.py`
3. **Regenerate visualization:**
   ```bash
   jupyter nbconvert --execute --to notebook --inplace notebooks/network_visualization.ipynb
   open outputs/network_map.html
   ```

## Troubleshooting

**"Failed to load" error?**
- Check that sheet is publicly readable (step 1)
- Verify gid values are correct (step 2)

**Funders not appearing?**
- Check the gid for "Funder List" tab
- Make sure column names match (Organization, Status, etc.)

**Need to update gids?**
- Click each tab and check the URL: `#gid=XXXXXXX`
- Update `SHEET_IDS` in `scripts/sync_from_sheets.py`
