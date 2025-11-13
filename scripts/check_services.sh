#!/bin/bash

# SSI System Health Check Script
# Verifies all services are running correctly

set -e

echo "🔍 Checking SSI System Health..."
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service health
check_service() {
    local name=$1
    local url=$2
    local expected=$3
    
    if curl -s "$url" | grep -q "$expected"; then
        echo -e "${GREEN}✅ $name: Running${NC}"
        return 0
    else
        echo -e "${RED}❌ $name: Not responding${NC}"
        return 1
    fi
}

# Function to check port
check_port() {
    local name=$1
    local port=$2
    
    if nc -z localhost "$port" 2>/dev/null; then
        echo -e "${GREEN}✅ $name (Port $port): Listening${NC}"
        return 0
    else
        echo -e "${RED}❌ $name (Port $port): Not listening${NC}"
        return 1
    fi
}

echo ""
echo "Checking Infrastructure Services..."
echo "-----------------------------------"

# Check Indy Ledger
check_service "Indy Ledger" "http://localhost:9000/status" "ready"

# Check PostgreSQL
check_port "PostgreSQL" "5432"

# Check IPFS
check_service "IPFS" "http://localhost:5001/api/v0/version" "Version"

echo ""
echo "Checking Agent Services..."
echo "--------------------------"

# Check Issuer Agent
check_service "Issuer Agent" "http://localhost:8030/status" "version"

# Check Holder Agent
check_service "Holder Agent" "http://localhost:8031/status" "version"

# Check Verifier Agent
check_service "Verifier Agent" "http://localhost:8032/status" "version"

echo ""
echo "Checking Database Connection..."
echo "-------------------------------"

# Check database tables exist
if psql postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB} -c "\dt" &>/dev/null; then
    echo -e "${GREEN}✅ Database: Connected${NC}"
else
    echo -e "${RED}❌ Database: Connection failed${NC}"
fi

echo ""
echo "Checking DID Registration..."
echo "----------------------------"

# Check if issuer DID is registered
ISSUER_DID=$(curl -s http://localhost:8030/wallet/did/public | jq -r '.result.did' 2>/dev/null)
if [ -n "$ISSUER_DID" ] && [ "$ISSUER_DID" != "null" ]; then
    echo -e "${GREEN}✅ Issuer DID: $ISSUER_DID${NC}"
else
    echo -e "${RED}❌ Issuer DID: Not registered${NC}"
fi

# Check if verifier DID is registered
VERIFIER_DID=$(curl -s http://localhost:8032/wallet/did/public | jq -r '.result.did' 2>/dev/null)
if [ -n "$VERIFIER_DID" ] && [ "$VERIFIER_DID" != "null" ]; then
    echo -e "${GREEN}✅ Verifier DID: $VERIFIER_DID${NC}"
else
    echo -e "${RED}❌ Verifier DID: Not registered${NC}"
fi

echo ""
echo "Checking Frontend..."
echo "-------------------"

# Check if frontend is running (if applicable)
if check_port "Frontend" "3000" 2>/dev/null; then
    echo -e "${GREEN}✅ Frontend: Running${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend: Not running (optional)${NC}"
fi

echo ""
echo "================================"
echo "Health Check Complete!"
echo ""

# Summary
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All critical services are running!${NC}"
    exit 0
else
    echo -e "${RED}Some services are not running. Please check the logs.${NC}"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f [service-name]"
    echo ""
    echo "To restart services:"
    echo "  docker-compose restart"
    exit 1
fi
