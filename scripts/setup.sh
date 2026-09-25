#!/bin/bash

# Apex Intelligence Server Setup
# This script sets up a private server for Apex Intelligence

set -e

echo "🚀 Apex Intelligence - Private Server Setup"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker Compose found: $(docker-compose --version)"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys and credentials"
fi

# Create logs directory
mkdir -p logs

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build

# Start services
echo "🏃 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if API is running
echo "🔍 Checking API health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ API is running!"
        break
    fi
    echo "Attempt $i/30..."
    sleep 1
done

echo ""
echo "✅ Apex Intelligence Private Server is running!"
echo ""
echo "📋 Service URLs:"
echo "   API:              http://localhost:8000"
echo "   API Docs:         http://localhost:8000/docs"
echo "   Supervisor:       http://localhost:9001"
echo "   Celery Flower:    http://localhost:5555"
echo ""
echo "📊 Database:"
echo "   PostgreSQL:       localhost:5432"
echo "   Redis:            localhost:6379"
echo ""
echo "🔐 Your server is private and running locally."
echo "To access from other machines, use your server IP address."
echo ""
echo "💡 View logs: docker-compose logs -f"
echo "🛑 Stop server: docker-compose down"
echo ""
