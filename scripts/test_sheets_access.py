#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pandas"]
# ///
"""
Quick test to check Google Sheets access and find sheet IDs (gids).
"""

import pandas as pd
import sys

SPREADSHEET_ID = "1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc"

def test_gid(gid, name=""):
    """Test if a gid is accessible."""
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        print(f"✓ gid={gid} {f'({name})' if name else ''}: {len(df)} rows, {len(df.columns)} columns")
        print(f"  Columns: {', '.join(df.columns.tolist()[:5])}{'...' if len(df.columns) > 5 else ''}")
        return True
    except Exception as e:
        print(f"✗ gid={gid} {f'({name})' if name else ''}: {str(e)[:80]}")
        return False

def main():
    print("="*60)
    print("Testing Google Sheets Access")
    print("="*60 + "\n")

    # Test known gid from URL
    print("Testing gid from URL (941366450)...")
    if test_gid("941366450", "from URL"):
        print("\n✓ Sheet is accessible!\n")
    else:
        print("\n✗ Sheet is NOT accessible!")
        print("\nTo fix:")
        print("1. Open: https://docs.google.com/spreadsheets/d/1G1b8zy-aWqFBeeBIgBMXgnZQI81du6wp8hieei2hkTc/")
        print("2. Click 'Share' → Change to 'Anyone with the link' → Viewer")
        print("3. Re-run this script\n")
        return

    # Try common gid values for other tabs
    print("\nTrying common gid values for other tabs...")
    test_gid("0", "often first tab")
    test_gid("1", "sometimes second tab")
    test_gid("2", "sometimes third tab")

    print("\n" + "="*60)
    print("Next steps:")
    print("="*60)
    print("\n1. Check which gids worked above")
    print("2. Open your sheet and click each tab to find the exact gid in URL")
    print("   Look for: #gid=XXXXXXX")
    print("3. Update scripts/sync_from_sheets.py with the correct gids")
    print("4. Run: ./scripts/sync_from_sheets.py\n")

if __name__ == "__main__":
    main()
