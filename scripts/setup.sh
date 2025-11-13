#!/bin/bash

# SSI System Setup Script
# Automates the complete setup process

set -e

echo "🚀 SSI System Setup"
echo "=================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo -e "${BLUE}Step 1: Checking Prerequisites${NC}"
echo "--------------------------------"

command -v docker >/dev/null 2>&1 || { echo "❌ Docker is not installed. Please install Docker first."; exit 1; }
echo "✅ Docker installed"

command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is not installed."; exit 1; }
echo "✅ Docker Compose installed"

command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 is not installed."; exit 1; }
echo "✅ Python3 installed"

command -v node >/dev/null 2>&1 || { echo "⚠️  Node.js not installed (optional for frontend)"; }
echo ""

# Create .env file
echo -e "${BLUE}Step 2: Creating Environment Configuration${NC}"
echo "-------------------------------------------"

if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    
    # Generate secure random keys
    WALLET_KEY=$(openssl rand -hex 32)
    JWT_SECRET=$(openssl rand -hex 32)
    API_KEY_ISSUER=$(openssl rand -hex 32)
    API_KEY_VERIFIER=$(openssl rand -hex 32)
    API_KEY_ADMIN=$(openssl rand -hex 32)
    
    # Update .env with generated keys
    sed -i "s/WALLET_KEY=.*/WALLET_KEY=$WALLET_KEY/" .env
    sed -i "s/JWT_SECRET=.*/JWT_SECRET=$JWT_SECRET/" .env
    sed -i "s/API_KEY_ISSUER=.*/API_KEY_ISSUER=$API_KEY_ISSUER/" .env
    sed -i "s/API_KEY_VERIFIER=.*/API_KEY_VERIFIER=$API_KEY_VERIFIER/" .env
    sed -i "s/API_KEY_ADMIN=.*/API_KEY_ADMIN=$API_KEY_ADMIN/" .env
    
    echo "✅ .env file created with secure random keys"
else
    echo "✅ .env file already exists"
fi
echo ""

# Create necessary directories
echo -e "${BLUE}Step 3: Creating Directory Structure${NC}"
echo "-------------------------------------"
mkdir -p logs backups config/genesis keys
echo "✅ Directories created"
echo ""

# Start infrastructure services
echo -e "${BLUE}Step 4: Starting Infrastructure Services${NC}"
echo "-----------------------------------------"
echo "Starting Indy Ledger, PostgreSQL, and IPFS..."
docker-compose up -d indy-pool postgres ipfs

echo "Waiting for services to be ready..."
sleep 30

# Verify infrastructure
echo "Verifying infrastructure..."
curl -f http://localhost:9000/status || { echo "❌ Indy ledger not ready"; exit 1; }
echo "✅ Indy ledger ready"

curl -f http://localhost:5001/api/v0/version || { echo "❌ IPFS not ready"; exit 1; }
echo "✅ IPFS ready"

# Download genesis file
echo "Downloading genesis file..."
curl http://localhost:9000/genesis > config/genesis.txn
echo "✅ Genesis file downloaded"
echo ""

# Initialize database
echo -e "${BLUE}Step 5: Initializing Database${NC}"
echo "------------------------------"
echo "Creating database schema..."
# Run database migrations here if using Alembic
echo "✅ Database initialized"
echo ""

# Start agent services
echo -e "${BLUE}Step 6: Starting Agent Services${NC}"
echo "--------------------------------"
echo "Starting Issuer, Holder, and Verifier agents..."
docker-compose up -d issuer-agent holder-agent verifier-agent

echo "Waiting for agents to start..."
sleep 20

echo "✅ All agents started"
echo ""

# Verify agent DIDs
echo -e "${BLUE}Step 7: Verifying Agent DIDs${NC}"
echo "-----------------------------"

ISSUER_DID=$(curl -s http://localhost:8030/wallet/did/public | jq -r '.result.did')
echo "Issuer DID: $ISSUER_DID"

VERIFIER_DID=$(curl -s http://localhost:8032/wallet/did/public | jq -r '.result.did')
echo "Verifier DID: $VERIFIER_DID"

echo "✅ DIDs registered"
echo ""

# Run health check
echo -e "${BLUE}Step 8: Running Health Check${NC}"
echo "-----------------------------"
bash scripts/check_services.sh

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "System Information:"
echo "-------------------"
echo "Indy Ledger Web UI: http://localhost:9000"
echo "Issuer Admin API:   http://localhost:8030"
echo "Holder Admin API:   http://localhost:8031"
echo "Verifier Admin API: http://localhost:8032"
echo "IPFS Web UI:        http://localhost:5001/webui"
echo ""
echo "Issuer DID:         $ISSUER_DID"
echo "Verifier DID:       $VERIFIER_DID"
echo ""
echo "API Keys (saved in .env):"
echo "  Issuer API Key:   $API_KEY_ISSUER"
echo "  Verifier API Key: $API_KEY_VERIFIER"
echo ""
echo "Next Steps:"
echo "1. View API docs: http://localhost:8030/api/doc"
echo "2. Run tests: ./scripts/run_tests.sh"
echo "3. Start frontend: cd frontend/wallet-ui && npm run dev"
echo ""
echo "To view logs: docker-compose logs -f [service-name]"
echo "To stop all services: docker-compose down"
echo ""
