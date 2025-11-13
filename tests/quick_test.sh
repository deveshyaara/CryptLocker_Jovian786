#!/bin/bash

# Quick Manual API Testing Script
# Use this for quick spot-checks without running full test suite

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           CryptLocker Quick API Test                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test Issuer Agent
echo -e "${BLUE}━━━ Issuer Agent Tests ━━━${NC}"

echo "1. Issuer Agent Health:"
curl -s http://localhost:11001/status/ready | jq .
echo ""

echo "2. Get Public DID:"
curl -s http://localhost:8001/did/public | jq .
echo ""

echo "3. List Schemas:"
curl -s http://localhost:8001/schema/list | jq '.schemas | length'
echo " schemas found"
echo ""

echo "4. List Credential Definitions:"
curl -s http://localhost:8001/credential-definition/list | jq '.credential_definitions | length'
echo " credential definitions found"
echo ""

echo "5. List Connections:"
curl -s http://localhost:8001/connection/list | jq '.connections | length'
echo " connections found"
echo ""

# Test Verifier Agent
echo -e "${BLUE}━━━ Verifier Agent Tests ━━━${NC}"

echo "6. Verifier Agent Health:"
curl -s http://localhost:11002/status/ready | jq .
echo ""

echo "7. Get Verifier Public DID:"
curl -s http://localhost:8002/did/public | jq .
echo ""

echo "8. List Verifier Connections:"
curl -s http://localhost:8002/connection/list | jq '.connections | length'
echo " connections found"
echo ""

# Test IPFS
echo -e "${BLUE}━━━ IPFS Tests ━━━${NC}"

echo "9. IPFS Node Info:"
curl -s -X POST http://localhost:5001/api/v0/id | jq '{ID: .ID, AgentVersion: .AgentVersion}'
echo ""

echo "10. IPFS Repo Stats:"
curl -s -X POST http://localhost:5001/api/v0/stats/repo | jq '{NumObjects: .NumObjects, RepoSize: .RepoSize}'
echo ""

# Test Indy Ledger
echo -e "${BLUE}━━━ Indy Ledger Tests ━━━${NC}"

echo "11. Genesis File Size:"
GENESIS_SIZE=$(curl -s http://localhost:9000/genesis | wc -c)
echo "${GENESIS_SIZE} bytes"
echo ""

# Summary
echo -e "${GREEN}━━━ Quick Test Complete ━━━${NC}"
echo ""
echo "For comprehensive testing, run:"
echo "  ./tests/run_health_check.sh"
echo ""
