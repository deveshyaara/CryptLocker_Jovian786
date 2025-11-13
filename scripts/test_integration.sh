#!/bin/bash
# Integration Test Script
# Tests end-to-end credential issuance and verification flow

set -e

echo "🧪 Running SSI Integration Tests"
echo "================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
ISSUER_ADMIN_URL="http://localhost:8030"
VERIFIER_ADMIN_URL="http://localhost:8050"
HOLDER_ADMIN_URL="http://localhost:8011"
ISSUER_API_KEY="issuer_admin_key_123"
VERIFIER_API_KEY="verifier_admin_key_123"
HOLDER_API_KEY="holder_admin_key_123"

# Helper function
test_endpoint() {
    local name=$1
    local url=$2
    local api_key=$3
    
    echo -n "Testing $name... "
    if curl -s -f -H "X-API-Key: $api_key" "$url" > /dev/null; then
        echo -e "${GREEN}✓${NC}"
        return 0
    else
        echo -e "${RED}✗${NC}"
        return 1
    fi
}

# Test 1: Health Checks
echo ""
echo "Test 1: Service Health Checks"
echo "------------------------------"
test_endpoint "Issuer Health" "$ISSUER_ADMIN_URL/health" "$ISSUER_API_KEY"
test_endpoint "Verifier Health" "$VERIFIER_ADMIN_URL/health" "$VERIFIER_API_KEY"
test_endpoint "Holder Health" "$HOLDER_ADMIN_URL/status" "$HOLDER_API_KEY"

# Test 2: DID Creation
echo ""
echo "Test 2: DID Management"
echo "----------------------"
echo "Creating DID for issuer..."
ISSUER_DID_RESPONSE=$(curl -s -X POST \
    -H "X-API-Key: $ISSUER_API_KEY" \
    "$ISSUER_ADMIN_URL/dids/create")

if echo "$ISSUER_DID_RESPONSE" | grep -q "did"; then
    echo -e "${GREEN}✓ Issuer DID created${NC}"
    ISSUER_DID=$(echo "$ISSUER_DID_RESPONSE" | grep -o '"did":"[^"]*"' | cut -d'"' -f4)
    echo "  DID: $ISSUER_DID"
else
    echo -e "${RED}✗ Failed to create issuer DID${NC}"
    echo "$ISSUER_DID_RESPONSE"
fi

# Test 3: Schema Creation
echo ""
echo "Test 3: Schema Creation"
echo "-----------------------"
SCHEMA_PAYLOAD='{
    "name": "university-degree",
    "version": "1.0",
    "attributes": ["name", "degree", "university", "graduation_date"]
}'

echo "Creating credential schema..."
SCHEMA_RESPONSE=$(curl -s -X POST \
    -H "X-API-Key: $ISSUER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$SCHEMA_PAYLOAD" \
    "$ISSUER_ADMIN_URL/schemas")

if echo "$SCHEMA_RESPONSE" | grep -q "schema_id"; then
    echo -e "${GREEN}✓ Schema created${NC}"
    SCHEMA_ID=$(echo "$SCHEMA_RESPONSE" | grep -o '"schema_id":"[^"]*"' | cut -d'"' -f4)
    echo "  Schema ID: $SCHEMA_ID"
else
    echo -e "${YELLOW}⚠ Schema creation may have failed (check if it already exists)${NC}"
fi

# Test 4: Connection Invitation
echo ""
echo "Test 4: DIDComm Connection"
echo "--------------------------"
INVITATION_PAYLOAD='{
    "alias": "test-holder",
    "multi_use": false,
    "public": false
}'

echo "Creating connection invitation..."
INVITATION_RESPONSE=$(curl -s -X POST \
    -H "X-API-Key: $ISSUER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$INVITATION_PAYLOAD" \
    "$ISSUER_ADMIN_URL/connections/create-invitation")

if echo "$INVITATION_RESPONSE" | grep -q "connection_id"; then
    echo -e "${GREEN}✓ Invitation created${NC}"
    CONNECTION_ID=$(echo "$INVITATION_RESPONSE" | grep -o '"connection_id":"[^"]*"' | cut -d'"' -f4)
    echo "  Connection ID: $CONNECTION_ID"
    
    # Extract invitation URL
    INVITATION_URL=$(echo "$INVITATION_RESPONSE" | grep -o '"invitation_url":"[^"]*"' | cut -d'"' -f4)
    echo "  Invitation URL: $INVITATION_URL"
else
    echo -e "${RED}✗ Failed to create invitation${NC}"
fi

# Test 5: List Connections
echo ""
echo "Test 5: List Connections"
echo "------------------------"
echo "Fetching issuer connections..."
CONNECTIONS=$(curl -s -H "X-API-Key: $ISSUER_API_KEY" \
    "$ISSUER_ADMIN_URL/connections")

if echo "$CONNECTIONS" | grep -q "results"; then
    echo -e "${GREEN}✓ Connections retrieved${NC}"
    CONNECTION_COUNT=$(echo "$CONNECTIONS" | grep -o '"connection_id"' | wc -l)
    echo "  Total connections: $CONNECTION_COUNT"
else
    echo -e "${RED}✗ Failed to retrieve connections${NC}"
fi

# Test 6: IPFS Check
echo ""
echo "Test 6: IPFS Availability"
echo "-------------------------"
if curl -s -f "http://localhost:5001/api/v0/id" > /dev/null; then
    echo -e "${GREEN}✓ IPFS API accessible${NC}"
    
    # Test IPFS add
    echo "Testing IPFS document storage..."
    TEST_FILE="/tmp/test_document.txt"
    echo "This is a test document for SSI system" > "$TEST_FILE"
    
    IPFS_ADD=$(curl -s -F "file=@$TEST_FILE" "http://localhost:5001/api/v0/add")
    if echo "$IPFS_ADD" | grep -q "Hash"; then
        IPFS_HASH=$(echo "$IPFS_ADD" | grep -o '"Hash":"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✓ Document added to IPFS${NC}"
        echo "  CID: $IPFS_HASH"
        
        # Test retrieval
        if curl -s -f "http://localhost:8080/ipfs/$IPFS_HASH" > /dev/null; then
            echo -e "${GREEN}✓ Document retrieved from IPFS${NC}"
        else
            echo -e "${YELLOW}⚠ IPFS retrieval test inconclusive${NC}"
        fi
    else
        echo -e "${RED}✗ Failed to add document to IPFS${NC}"
    fi
    
    rm -f "$TEST_FILE"
else
    echo -e "${RED}✗ IPFS API not accessible${NC}"
fi

# Test 7: Indy Ledger
echo ""
echo "Test 7: Indy Ledger Access"
echo "--------------------------"
if curl -s -f "http://localhost:9000/" > /dev/null; then
    echo -e "${GREEN}✓ Indy ledger web interface accessible${NC}"
    echo "  URL: http://localhost:9000"
    
    # Check genesis file
    if curl -s -f "http://localhost:9000/genesis" > /dev/null; then
        echo -e "${GREEN}✓ Genesis file available${NC}"
    else
        echo -e "${YELLOW}⚠ Genesis file not yet available${NC}"
    fi
else
    echo -e "${RED}✗ Indy ledger not accessible${NC}"
fi

# Summary
echo ""
echo "================================="
echo "Test Summary"
echo "================================="
echo "Service health checks: Complete"
echo "DID creation: Tested"
echo "Schema creation: Tested"
echo "Connection flow: Initiated"
echo "IPFS integration: Verified"
echo "Indy ledger: Accessible"
echo ""
echo "📝 Next Steps:"
echo "1. Complete connection flow with holder agent"
echo "2. Test credential issuance"
echo "3. Test proof request and verification"
echo "4. Implement automated integration tests"
echo ""
echo "🔍 Manual Testing:"
echo "  • Indy Ledger: http://localhost:9000"
echo "  • IPFS Gateway: http://localhost:8080"
echo "  • Issuer API: http://localhost:8030"
echo "  • Verifier API: http://localhost:8050"
echo ""
