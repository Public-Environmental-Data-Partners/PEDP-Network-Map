# PEDP Network Map - Quick Reference

## Daily Workflow (Google Sheets)

```bash
# 1. Edit your Google Sheet
#    https://docs.google.com/spreadsheets/d/1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc/

# 2. Sync to CSV
./scripts/sync_from_sheets.py

# 3. Regenerate visualization
jupyter nbconvert --execute --to notebook --inplace notebooks/network_visualization.ipynb

# 4. View
open outputs/network_map.html
```

## One-Time Setup

See `SHEETS_SETUP.md` for detailed instructions.

**Quick version:**
1. Make sheet public (Share → Anyone with link → Viewer)
2. Find gid values (click tabs, check URL: #gid=XXX)
3. Update `scripts/sync_from_sheets.py` with gids

## File Structure

```
data/processed/
  ├── nodes.csv     ← Node data (auto-generated from Sheets)
  ├── edges.csv     ← Edge data (auto-generated from Sheets)
  └── colors.csv    ← Color palette (edit to change colors)

scripts/
  ├── sync_from_sheets.py      ← Main sync script
  └── test_sheets_access.py    ← Test connection

notebooks/
  └── network_visualization.ipynb  ← Generates HTML

outputs/
  └── network_map.html  ← Final visualization
```

## Funder List Rules

| Status | Node | Edge to PEDP |
|--------|------|--------------|
| 0. On our radar | ✓ | ✗ |
| 1. In conversation | ✓ | ✗ |
| 2. Proposal submitted | ✓ | ✗ |
| 4. approved | ✓ | ✓ |

## Color Customization

Edit `data/processed/colors.csv`:
```csv
name,hex
red,#e74c3c     ← Change hex codes here
green,#2ecc71   ← All nodes using this color update
teal,#1abc9c    ← Used for funders
```

## Troubleshooting

**Sync fails?**
- Check sheet is public: `./scripts/test_sheets_access.py`
- Verify gid values in `scripts/sync_from_sheets.py`

**Colors not working?**
- Make sure color names in `nodes.csv` match `colors.csv`

**Need help?**
- Setup: `SHEETS_SETUP.md`
- Editing: `EDITING_GUIDE.md`
- Full docs: `README.md`
