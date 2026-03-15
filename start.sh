#!/bin/bash
# Cost of Living - Quick Start Script
# Requires: MkDocs Material
# pip install mkdocs-material

echo "🪙 Cost of Living - Starting..."

# Check if mkdocs is installed
if command -v mkdocs &> /dev/null; then
    echo "✅ MkDocs found - starting server..."
    mkdocs serve --dev-addr 0.0.0.0:8080
else
    echo "❌ MkDocs not found"
    echo ""
    echo "Installing..."
    pip install mkdocs-material
    
    if [ $? -eq 0 ]; then
        echo "✅ Installed! Starting..."
        mkdocs serve --dev-addr 0.0.0.0:8080
    else
        echo "❌ Installation failed"
        echo ""
        echo "Alternative: Use Python simple server"
        echo "  python3 -m http.server 8080"
    fi
fi