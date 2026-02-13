#!/usr/bin/env python3
"""
Add visual indicators to hypothetical network HTML file.

Adds:
- Banner at top of page
- Watermark overlay
- Updated page title
- Grey background styling
"""

from bs4 import BeautifulSoup
import os

html_path = 'outputs/network_map_hypothetical.html'

# Check if file exists
if not os.path.exists(html_path):
    print(f"❌ Error: {html_path} not found")
    print("   Run the hypothetical visualization notebook first")
    exit(1)

print(f"Adding visual indicators to {html_path}...")

# Read generated HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 1. Update title
print("  • Updating page title...")
title_tag = soup.find('title')
if title_tag:
    title_tag.string = "PEDP Network - Hypothetical Future State (Scenario Analysis)"
else:
    # Create title tag if missing
    new_title = soup.new_tag('title')
    new_title.string = "PEDP Network - Hypothetical Future State (Scenario Analysis)"
    soup.head.append(new_title)

# 2. Add banner at top of body
print("  • Adding warning banner...")
banner_html = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            border-bottom: 3px solid #999;
            margin: 0;
            position: sticky;
            top: 0;
            z-index: 9999;">
    🔮 HYPOTHETICAL FUTURE STATE - NOT CURRENT NETWORK
    <div style="font-size: 14px; margin-top: 5px; font-weight: normal;">
        Scenario analysis showing potential network connectivity through intermediary organizations
    </div>
</div>
"""
banner_soup = BeautifulSoup(banner_html, 'html.parser')
soup.body.insert(0, banner_soup)

# 3. Add watermark CSS
print("  • Adding watermark overlay...")
watermark_css = """
<style>
/* Watermark overlay */
body::before {
    content: "SCENARIO ANALYSIS";
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 120px;
    color: rgba(150, 150, 150, 0.1);
    z-index: -1;
    pointer-events: none;
    font-weight: bold;
    white-space: nowrap;
}

/* Update canvas background to light grey */
#mynetwork {
    background-color: #f8f8f8 !important;
}

/* Add legend for hypothetical edges */
.hypothetical-legend {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.95);
    padding: 15px;
    border: 2px solid #999;
    border-radius: 8px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.hypothetical-legend h4 {
    margin: 0 0 10px 0;
    font-size: 16px;
    color: #333;
}

.hypothetical-legend .legend-item {
    margin: 5px 0;
    display: flex;
    align-items: center;
}

.hypothetical-legend .legend-line {
    width: 40px;
    height: 2px;
    margin-right: 10px;
    border-top: 2px dashed;
}

.hypothetical-legend .real-line {
    border-color: #3498db;
    border-style: solid;
}

.hypothetical-legend .hyp-line {
    border-color: #999999;
}
</style>
"""
soup.head.append(BeautifulSoup(watermark_css, 'html.parser'))

# 4. Add legend HTML
print("  • Adding edge type legend...")
legend_html = """
<div class="hypothetical-legend">
    <h4>Edge Types</h4>
    <div class="legend-item">
        <div class="legend-line real-line"></div>
        <span>Current relationships</span>
    </div>
    <div class="legend-item">
        <div class="legend-line hyp-line"></div>
        <span>Hypothetical connections</span>
    </div>
    <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
        Grey dashed lines = potential future partnerships
    </div>
</div>
"""
legend_soup = BeautifulSoup(legend_html, 'html.parser')
soup.body.append(legend_soup)

# Save modified HTML
print(f"  • Saving modified HTML...")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print(f"\n✅ Visual indicators added successfully!")
print(f"\nModifications:")
print(f"  ✓ Page title updated")
print(f"  ✓ Warning banner added at top")
print(f"  ✓ Watermark overlay added")
print(f"  ✓ Background changed to light grey")
print(f"  ✓ Legend added for edge types")
print(f"\nOutput: {html_path}")
