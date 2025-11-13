#!/bin/bash

# Complete System Startup Script
# Starts Indy ledger, PostgreSQL, IPFS, and all agents

set -e

echo "=========================================="
echo "Starting SSI System"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration!"
fi

# Step 1: Start Indy Network
echo ""
echo "Step 1/3: Starting Indy Network..."
bash infrastructure/scripts/start-indy-network.sh

# Wait for Indy network to be ready
echo "Waiting for Indy network to initialize..."
sleep 10

# Step 2: Start Docker services
echo ""
echo "Step 2/3: Starting Docker services (PostgreSQL, IPFS, Agents)..."
cd infrastructure
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to initialize..."
sleep 15

# Step 3: Health check
echo ""
echo "Step 3/3: Running health checks..."

check_service() {
    local url=$1
    local name=$2
    if curl -s -f "$url" > /dev/null; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is not responding"
    fi
}

check_service "http://localhost:9000" "Indy Ledger Browser"
check_service "http://localhost:8080/ipfs/QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn" "IPFS Gateway"
check_service "http://localhost:8000/health" "Issuer API"
check_service "http://localhost:8001/health" "Verifier API"

echo ""
echo "=========================================="
echo "SSI System Started Successfully!"
echo "=========================================="
echo ""
echo "Service URLs:"
echo "  📊 Indy Ledger Browser: http://localhost:9000"
echo "  🏛️  Issuer API: http://localhost:8000"
echo "  🔍 Verifier API: http://localhost:8001"
echo "  📦 IPFS Gateway: http://localhost:8080"
echo "  🗄️  PostgreSQL: localhost:5432"
echo ""
echo "API Documentation:"
echo "  📖 Issuer API Docs: http://localhost:8000/docs"
echo "  📖 Verifier API Docs: http://localhost:8001/docs"
echo ""
echo "To stop all services: bash infrastructure/scripts/stop-system.sh"
echo "=========================================="
