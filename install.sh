#!/bin/bash

# Make scripts executable
chmod +x scripts/*.sh

echo "Installing Apex Intelligence Private Server..."
echo ""

# Check requirements
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed. Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed. Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker & Docker Compose installed"
echo ""

# Create .env if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file (please update with your API keys)"
fi

# Create necessary directories
mkdir -p logs backups

echo ""
echo "🔨 Building Apex Intelligence container..."
docker-compose build

echo ""
echo "🚀 Starting Apex Intelligence Private Server..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "✅ Apex Intelligence is running!"
echo ""
echo "📋 Access points:"
echo "   API:              http://localhost:8000"
echo "   API Docs:         http://localhost:8000/docs"
echo "   Supervisor:       http://localhost:9001"
echo "   Celery Flower:    http://localhost:5555"
echo ""
echo "📊 Services:"
docker-compose ps
echo ""
echo "💡 Next steps:"
echo "   1. Update .env with your API keys"
echo "   2. Run: docker-compose restart"
echo "   3. Visit http://localhost:8000/docs for API docs"
echo ""
