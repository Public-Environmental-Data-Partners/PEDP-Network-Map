#!/bin/bash

# Build both current and hypothetical network visualizations
# This script orchestrates the complete build pipeline

set -e  # Exit on error

echo "=================================================="
echo "Building PEDP Network Visualizations"
echo "=================================================="
echo ""

# Step 1: Generate hypothetical network data
echo "Step 1: Generating hypothetical network data..."
python3 scripts/generate_hypothetical_network.py
echo ""

# Step 2: Build current network visualization
echo "Step 2: Building current network visualization..."
cd notebooks
jupyter nbconvert --execute --to notebook --inplace network_visualization.ipynb
cd ..
echo ""

# Step 3: Build hypothetical network visualization
echo "Step 3: Building hypothetical network visualization..."
python3 scripts/build_hypothetical_visualization.py
echo ""

# Step 4: Add hypothetical watermark/indicators
echo "Step 4: Adding visual indicators to hypothetical page..."
python3 scripts/add_hypothetical_watermark.py
echo ""

echo "=================================================="
echo "✅ Build Complete!"
echo "=================================================="
echo ""
echo "Output files:"
echo "  • Current network:      outputs/network_map.html"
echo "  • Hypothetical network: outputs/network_map_hypothetical.html"
echo ""
echo "To view:"
echo "  open outputs/network_map.html"
echo "  open outputs/network_map_hypothetical.html"
echo ""
echo "Compare side-by-side to see current vs future state!"
echo "=================================================="
