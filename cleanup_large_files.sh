#!/bin/bash

echo "🗑️  Removing large unnecessary files..."
echo ""

# Kaggle Data (7GB!) - Models sind bereits trainiert
echo "Removing kaggle_data (7GB)..."
rm -rf kaggle_data/

# Virtual Environment - wird lokal eh neu erstellt
echo "Removing venv (1.2GB)..."
rm -rf venv/

# Pycache
echo "Removing __pycache__..."
rm -rf __pycache__/

# Logs
echo "Removing logs..."
rm -rf logs/
rm -f api.log
rm -f *.log

# Cleanup script itself
rm -f cleanup_project.sh

echo ""
echo "✅ Large files cleanup complete!"
echo ""
echo "Checking remaining size..."
du -sh . 2>/dev/null

