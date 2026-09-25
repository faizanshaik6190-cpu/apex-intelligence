@echo off
title Apex Intelligence
set PYTHONUNBUFFERED=1

echo Installing dependencies...
python -m pip install PyQt6 requests --quiet

echo.
echo Starting Apex Intelligence...
echo.

python apex_intelligence.py

pause
