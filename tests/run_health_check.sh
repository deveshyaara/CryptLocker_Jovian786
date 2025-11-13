#!/bin/bash

# CryptLocker System Health Check Script
# Tests all completed components

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        CryptLocker System Health Check                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker services are running
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Step 1: Checking Docker Services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$(dirname "$0")"

if ! docker compose -f ../infrastructure/docker-compose.yml ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  Docker services not running. Starting services...${NC}"
    docker compose -f ../infrastructure/docker-compose.yml up -d
    echo "⏳ Waiting 30 seconds for services to initialize..."
    sleep 30
else
    echo -e "${GREEN}✅ Docker services are running${NC}"
fi

echo ""

# Check individual service health
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Step 2: Service Health Checks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_service() {
    local name=$1
    local url=$2
    local max_retries=5
    local retry=0
    
    while [ $retry -lt $max_retries ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $name is healthy${NC}"
            return 0
        fi
        retry=$((retry + 1))
        if [ $retry -lt $max_retries ]; then
            echo "   ⏳ Retry $retry/$max_retries for $name..."
            sleep 3
        fi
    done
    
    echo -e "${RED}❌ $name is not responding${NC}"
    return 1
}

check_service "Issuer Agent" "http://localhost:11001/status/ready"
check_service "Verifier Agent" "http://localhost:11002/status/ready"
check_service "IPFS Node" "http://localhost:5001/api/v0/id"
check_service "Indy Ledger" "http://localhost:9000/genesis"

echo ""

# Install test dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Step 3: Installing Test Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v pytest &> /dev/null; then
    echo "Installing pytest and dependencies..."
    pip install pytest pytest-asyncio httpx > /dev/null 2>&1
    echo -e "${GREEN}✅ Test dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Test dependencies already installed${NC}"
fi

echo ""

# Run integration tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Step 4: Running Integration Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd ..

pytest tests/integration/test_system_health.py -v --tb=short --color=yes

TEST_EXIT_CODE=$?

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo ""
    echo "System Status: HEALTHY ✅"
    echo ""
    echo "Completed Components:"
    echo "  ✅ Issuer Agent (13 endpoints)"
    echo "  ✅ Verifier Agent (12 endpoints)"
    echo "  ✅ IPFS Service"
    echo "  ✅ PostgreSQL Database"
    echo "  ✅ Indy Ledger (4-node testnet)"
    echo ""
    echo "Ready for: Sprint 3 (Holder Agent implementation)"
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo ""
    echo "Check logs above for details."
    echo "Common issues:"
    echo "  - Services not fully initialized (wait longer)"
    echo "  - Port conflicts"
    echo "  - Docker daemon not running"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $TEST_EXIT_CODE
