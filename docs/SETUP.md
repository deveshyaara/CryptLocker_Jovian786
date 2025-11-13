# 🚀 Setup Guide

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / macOS 12+ / Windows 10+ (WSL2)
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Disk**: 20GB free space
- **CPU**: 4+ cores recommended

### Required Software

#### 1. Docker & Docker Compose
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker

# macOS (using Homebrew)
brew install --cask docker

# Verify installation
docker --version  # Should be 20.10+
docker-compose --version  # Should be 1.29+
```

#### 2. Python 3.11+
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3-pip -y

# macOS
brew install python@3.11

# Verify installation
python3.11 --version
```

#### 3. Node.js 18+ (for frontend)
```bash
# Ubuntu/Debian (using NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# macOS
brew install node@18

# Verify installation
node --version  # Should be 18+
npm --version
```

#### 4. Poetry (Python package manager)
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

#### 5. Git
```bash
# Ubuntu/Debian
sudo apt install git -y

# macOS
brew install git

# Configure
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/deveshyaara/CryptLocker_Jovian786.git
cd CryptLocker_Jovian786
```

### 2. Start Indy Network
```bash
# Start local Indy ledger (von-network)
cd infrastructure/indy
docker-compose up -d

# Wait for network to be ready (30-60 seconds)
curl http://localhost:9000/status

# You should see: {"status": "ready"}
```

### 3. Initialize Agents
```bash
# Return to project root
cd ../..

# Start all agents (Issuer, Holder, Verifier)
cd agents
docker-compose up -d

# Verify agents are running
docker-compose ps

# Check agent logs
docker-compose logs -f issuer
```

### 4. Run Frontend
```bash
# Install dependencies
cd ../frontend/wallet-ui
npm install

# Start development server
npm run dev

# Open browser: http://localhost:3000
```

## Detailed Setup

### Step 1: Environment Configuration

Create environment files for each component:

#### `.env` (Root)
```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

```env
# Indy Ledger Configuration
INDY_GENESIS_URL=http://localhost:9000/genesis
INDY_POOL_NAME=local_pool

# Agent Configuration
ISSUER_AGENT_PORT=8020
HOLDER_AGENT_PORT=8021
VERIFIER_AGENT_PORT=8022

ISSUER_ADMIN_PORT=8030
HOLDER_ADMIN_PORT=8031
VERIFIER_ADMIN_PORT=8032

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ssi_vault
POSTGRES_USER=ssi_user
POSTGRES_PASSWORD=change_me_in_production

# IPFS Configuration
IPFS_API_URL=http://localhost:5001
IPFS_GATEWAY_URL=http://localhost:8080

# Security
WALLET_KEY=change_me_to_secure_random_32_char_key
JWT_SECRET=change_me_to_secure_random_jwt_secret
API_KEY=change_me_to_secure_random_api_key

# Environment
NODE_ENV=development
LOG_LEVEL=debug
```

#### `agents/issuer/.env`
```env
AGENT_NAME=issuer-agent
AGENT_PORT=8020
ADMIN_PORT=8030
ADMIN_API_KEY=${API_KEY}

WALLET_NAME=issuer-wallet
WALLET_KEY=${WALLET_KEY}
WALLET_TYPE=askar

GENESIS_URL=${INDY_GENESIS_URL}
PUBLIC_DID_SEED=issuer_seed_000000000000000000000

LOG_LEVEL=debug
AUTO_ACCEPT_REQUESTS=false
AUTO_RESPOND_CREDENTIAL_OFFER=false
```

### Step 2: Hyperledger Indy Setup

#### Option A: Local Development (von-network)
```bash
cd infrastructure/indy

# Start 4-node Indy network
docker-compose up -d

# Wait for startup
sleep 30

# Verify network health
curl http://localhost:9000/status
curl http://localhost:9000/genesis > ../../config/genesis.txn

# Access web interface
# Browser: http://localhost:9000
```

#### Option B: Sovrin Staging Network
```bash
# Download Sovrin StagingNet genesis file
curl https://raw.githubusercontent.com/sovrin-foundation/sovrin/master/sovrin/pool_transactions_sandbox_genesis -o config/genesis.txn

# Update .env
INDY_GENESIS_URL=file://$(pwd)/config/genesis.txn
INDY_POOL_NAME=sovrin_staging
```

### Step 3: Agent Setup

#### Initialize Issuer Agent
```bash
cd agents/issuer

# Install dependencies
poetry install

# Initialize wallet
poetry run python scripts/init_wallet.py

# Register DID on ledger
poetry run python scripts/register_did.py

# Start agent
poetry run aca-py start \
  --inbound-transport http 0.0.0.0 8020 \
  --outbound-transport http \
  --admin 0.0.0.0 8030 \
  --admin-insecure-mode \
  --wallet-type askar \
  --wallet-name issuer-wallet \
  --wallet-key ${WALLET_KEY} \
  --genesis-url ${INDY_GENESIS_URL} \
  --seed ${PUBLIC_DID_SEED} \
  --public-invites \
  --auto-provision \
  --log-level debug
```

#### Initialize Holder Agent (Similar for Verifier)
```bash
cd agents/holder

poetry install
poetry run python scripts/init_wallet.py

# Start agent
poetry run aca-py start \
  --inbound-transport http 0.0.0.0 8021 \
  --outbound-transport http \
  --admin 0.0.0.0 8031 \
  --admin-insecure-mode \
  --wallet-type askar \
  --wallet-name holder-wallet \
  --wallet-key ${WALLET_KEY} \
  --genesis-url ${INDY_GENESIS_URL} \
  --auto-provision \
  --log-level debug
```

### Step 4: Database Setup

```bash
cd infrastructure/database

# Start PostgreSQL
docker-compose up -d

# Wait for startup
sleep 10

# Run migrations
cd ../../agents/issuer
poetry run alembic upgrade head

# Verify
poetry run python scripts/verify_db.py
```

### Step 5: IPFS Setup

```bash
cd infrastructure/ipfs

# Start IPFS node
docker-compose up -d

# Wait for startup
sleep 10

# Test IPFS
curl -X POST http://localhost:5001/api/v0/version

# Access web UI: http://localhost:5001/webui
```

### Step 6: Frontend Setup

```bash
cd frontend/wallet-ui

# Install dependencies
npm install

# Generate API client from OpenAPI spec
npm run generate-api

# Start development server
npm run dev

# Build for production
npm run build
```

## Verification

### 1. Check All Services
```bash
# From project root
./scripts/check_services.sh
```

Expected output:
```
✅ Indy Ledger: Running
✅ Issuer Agent: Running (Port 8020)
✅ Holder Agent: Running (Port 8021)
✅ Verifier Agent: Running (Port 8022)
✅ PostgreSQL: Running (Port 5432)
✅ IPFS: Running (Port 5001)
✅ Frontend: Running (Port 3000)
```

### 2. Test DID Creation
```bash
curl -X POST http://localhost:8030/wallet/did/create \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{}'

# Should return: {"result": {"did": "did:indy:...", "verkey": "..."}}
```

### 3. Test Credential Schema Creation
```bash
curl -X POST http://localhost:8030/schemas \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "degree",
    "schema_version": "1.0",
    "attributes": ["name", "degree", "university", "graduation_date"]
  }'
```

### 4. Open Frontend
```bash
# Browser: http://localhost:3000

# You should see the wallet login page
```

## Troubleshooting

### Indy Ledger Issues

**Problem**: Cannot connect to ledger
```bash
# Check if network is running
docker ps | grep von-network

# Restart network
cd infrastructure/indy
docker-compose restart

# Check logs
docker-compose logs -f
```

**Problem**: Genesis file not found
```bash
# Download genesis file
curl http://localhost:9000/genesis > config/genesis.txn

# Update .env
INDY_GENESIS_URL=file://$(pwd)/config/genesis.txn
```

### Agent Issues

**Problem**: Agent won't start
```bash
# Check wallet initialization
poetry run python scripts/verify_wallet.py

# Reset wallet (WARNING: deletes all data)
poetry run python scripts/reset_wallet.py

# Check admin API
curl http://localhost:8030/status
```

**Problem**: "Wallet already exists" error
```bash
# Use existing wallet or delete it
rm -rf ~/.aries_cloudagent/wallet/${WALLET_NAME}

# Or set in .env:
AUTO_PROVISION=true
```

### Database Issues

**Problem**: Cannot connect to database
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check connection
psql postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}

# Reset database
cd infrastructure/database
docker-compose down -v
docker-compose up -d
```

### IPFS Issues

**Problem**: IPFS not responding
```bash
# Restart IPFS
cd infrastructure/ipfs
docker-compose restart

# Check API
curl http://localhost:5001/api/v0/id
```

### Frontend Issues

**Problem**: Build failures
```bash
# Clear cache
npm run clean
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

## Development Tools

### VS Code Extensions (Recommended)
```bash
# Install recommended extensions
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension ms-azuretools.vscode-docker
```

### CLI Tools
```bash
# Install ACA-Py CLI tools
pip install aries-cloudagent-cli

# Install Indy CLI
pip install indy-cli

# Install jq for JSON processing
sudo apt install jq -y  # Ubuntu
brew install jq  # macOS
```

## Next Steps

1. ✅ Complete setup verification
2. 📖 Read [API Documentation](./docs/api/)
3. 🏗️ Follow [Development Guide](./docs/guides/development.md)
4. 🧪 Run test suite: `./scripts/run_tests.sh`
5. 🚀 Start building!

## Support

- **Issues**: https://github.com/deveshyaara/CryptLocker_Jovian786/issues
- **Discussions**: https://github.com/deveshyaara/CryptLocker_Jovian786/discussions
- **Docs**: https://github.com/deveshyaara/CryptLocker_Jovian786/wiki

---

Setup time: ~15-30 minutes (depending on internet speed)
