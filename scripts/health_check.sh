#!/bin/bash

# Apex Intelligence - Health Check

echo "🏥 Apex Intelligence Health Check"
echo "==================================="

echo ""
echo "🔍 Checking API..."
curl -s http://localhost:8000/health | python -m json.tool

echo ""
echo "🔍 Checking CEO Summary..."
curl -s http://localhost:8000/ceo/summary | python -m json.tool

echo ""
echo "🔍 Checking Docker containers..."
docker ps --filter "name=apex" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "✅ Health check complete"
