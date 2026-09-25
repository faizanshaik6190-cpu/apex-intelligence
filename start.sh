#!/bin/bash
export PYTHONUNBUFFERED=1

echo "Installing dependencies..."
python3 -m pip install PyQt6 requests --quiet

echo ""
echo "Starting Apex Intelligence..."
echo ""

python3 apex_intelligence.py
