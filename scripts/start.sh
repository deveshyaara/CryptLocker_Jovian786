#!/bin/bash
# Quick Start Script for SSI System
# Initializes the development environment and starts all services

set -e

echo "🚀 Starting Decentralized Digital Identity & Credential Vault"
echo "=============================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created. Please review and update with secure values!${NC}"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

echo ""
echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🏗️  Starting infrastructure services (Indy, PostgreSQL, IPFS)..."
docker-compose up -d indy-pool postgres ipfs

echo ""
echo "⏳ Waiting for infrastructure to be healthy (this may take 2-3 minutes)..."
sleep 20

# Check service health
echo "🔍 Checking Indy Pool..."
timeout 120 bash -c 'until docker-compose exec -T indy-pool curl -f http://localhost:8000/ 2>/dev/null; do sleep 5; done' || {
    echo -e "${RED}❌ Indy Pool failed to start${NC}"
    docker-compose logs indy-pool
    exit 1
}
echo -e "${GREEN}✅ Indy Pool is ready${NC}"

echo "🔍 Checking PostgreSQL..."
docker-compose exec -T postgres pg_isready -U ssi_user || {
    echo -e "${RED}❌ PostgreSQL failed to start${NC}"
    docker-compose logs postgres
    exit 1
}
echo -e "${GREEN}✅ PostgreSQL is ready${NC}"

echo "🔍 Checking IPFS..."
docker-compose exec -T ipfs ipfs id >/dev/null 2>&1 || {
    echo -e "${RED}❌ IPFS failed to start${NC}"
    docker-compose logs ipfs
    exit 1
}
echo -e "${GREEN}✅ IPFS is ready${NC}"

echo ""
echo "🚀 Starting agent services..."
docker-compose up -d issuer-agent holder-agent verifier-agent

echo ""
echo "⏳ Waiting for agents to initialize (30 seconds)..."
sleep 30

echo ""
echo "=============================================================="
echo -e "${GREEN}✨ SSI System is running!${NC}"
echo "=============================================================="
echo ""
echo "📊 Service URLs:"
echo "  • Indy Pool Web Interface:  http://localhost:9000"
echo "  • IPFS Gateway:             http://localhost:8080"
echo "  • Issuer Agent Admin API:   http://localhost:8030"
echo "  • Holder Agent Admin API:   http://localhost:8011"
echo "  • Verifier Agent Admin API: http://localhost:8050"
echo ""
echo "🔍 Check service status:"
echo "  docker-compose ps"
echo ""
echo "📋 View logs:"
echo "  docker-compose logs -f [service-name]"
echo ""
echo "🛑 Stop all services:"
echo "  docker-compose down"
echo ""
echo "🗑️  Clean everything (including data):"
echo "  docker-compose down -v"
echo ""
echo "=============================================================="
