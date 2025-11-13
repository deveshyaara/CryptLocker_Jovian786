# 🚀 Quick Start Guide
# CryptLocker - Decentralized Digital Identity & Credential Vault

Get the complete SSI system running in under 10 minutes.

---

## Prerequisites

```bash
# Required software
docker --version          # Docker 20.10+ required
docker-compose --version  # Docker Compose 1.29+ required
git --version            # Git 2.30+ required
curl --version           # For health checks

# Optional (for local development)
python --version         # Python 3.11+ for running tests
node --version           # Node.js 18+ for mobile wallet (Sprint 3+)
```

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/deveshyaara/CryptLocker_Jovian786.git
cd CryptLocker_Jovian786
```

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your keys (REQUIRED for production)
nano .env

# Minimum changes needed:
# - ISSUER_ADMIN_API_KEY=<generate-strong-key>
# - VERIFIER_ADMIN_API_KEY=<generate-strong-key>
# - POSTGRES_PASSWORD=<generate-strong-password>
# - ISSUER_WALLET_KEY=<32-character-minimum>
# - VERIFIER_WALLET_KEY=<32-character-minimum>
```

### Step 3: Start System
```bash
# Make scripts executable
chmod +x infrastructure/scripts/*.sh

# Start complete system (Indy + Docker services)
bash infrastructure/scripts/start-system.sh

# This will:
# 1. Clone and start von-network (4-node Indy ledger)
# 2. Start PostgreSQL, IPFS, and agents
# 3. Run health checks
# 4. Display service URLs
```

**Wait time**: ~30-45 seconds for all services to initialize

---

## Verification

### Check Service Health

```bash
# Indy Ledger Browser
curl http://localhost:9000
# Should return HTML page

# Issuer API Health
curl http://localhost:8000/health
# Expected: {"status":"healthy","acapy":"connected"}

# Verifier API Health
curl http://localhost:8001/health
# Expected: {"status":"healthy","acapy":"connected"}

# IPFS Gateway
curl http://localhost:8080/ipfs/QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn
# Should return IPFS readme

# PostgreSQL
docker exec -it ssi-postgres psql -U postgres -c "SELECT version();"
# Should show PostgreSQL 15.x
```

### Access Web UIs

Open in your browser:
- **Indy Ledger Browser**: http://localhost:9000
- **Issuer API Documentation**: http://localhost:8000/docs
- **Verifier API Documentation**: http://localhost:8001/docs
- **IPFS Web UI**: http://localhost:5001/webui (if enabled)

---

## Usage Examples

### Example 1: Create DID (Issuer)

```bash
# Create a new DID
curl -X POST http://localhost:8000/dids/create \
  -H "X-API-Key: issuer-api-key-change-me-in-production" \
  -H "Content-Type: application/json"

# Response:
# {
#   "did": "did:indy:local:WRfXPg8dantKVubE3HX8pw",
#   "verkey": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL",
#   "posture": "wallet_only"
# }
```

### Example 2: Create Schema

```bash
# Create university degree schema
curl -X POST http://localhost:8000/schemas \
  -H "X-API-Key: issuer-api-key-change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "university-degree",
    "version": "1.0",
    "attributes": ["name", "degree", "university", "graduation_date"]
  }'

# Response includes schema_id:
# {
#   "schema_id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
#   "schema": {...}
# }
```

### Example 3: Create Credential Definition

```bash
# Create credential definition for schema
curl -X POST http://localhost:8000/credential-definitions \
  -H "X-API-Key: issuer-api-key-change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "schema_id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
    "tag": "default",
    "support_revocation": true
  }'

# Response includes credential_definition_id
```

### Example 4: Create Connection Invitation

```bash
# Issuer creates invitation for holder
curl -X POST http://localhost:8000/connections/create-invitation \
  -H "X-API-Key: issuer-api-key-change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "Alice Student",
    "multi_use": false
  }'

# Response includes invitation_url (QR code for mobile wallet)
# {
#   "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#   "invitation_url": "http://example.com?c_i=eyJAdHlwZSI6Li4u",
#   "invitation": {...}
# }
```

### Example 5: Issue Credential

```bash
# Issue degree credential to connected holder
curl -X POST http://localhost:8000/credentials/issue \
  -H "X-API-Key: issuer-api-key-change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "cred_def_id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default",
    "attributes": [
      {"name": "name", "value": "Alice Smith"},
      {"name": "degree", "value": "Bachelor of Science"},
      {"name": "university", "value": "MIT"},
      {"name": "graduation_date", "value": "2023-06-15"}
    ],
    "comment": "University Degree"
  }'

# Returns credential_exchange_id for tracking
```

### Example 6: Request Proof (Verifier)

```bash
# Verifier requests proof of degree
curl -X POST http://localhost:8001/proof-requests/send \
  -H "X-API-Key: verifier-api-key-change-me-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "verifier-holder-connection-id",
    "name": "Employment Verification",
    "version": "1.0",
    "requested_attributes": {
      "attr1_referent": {
        "name": "degree",
        "restrictions": [
          {"cred_def_id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default"}
        ]
      }
    },
    "requested_predicates": {
      "pred1_referent": {
        "name": "graduation_date",
        "p_type": ">=",
        "p_value": 2020,
        "restrictions": []
      }
    }
  }'

# Returns presentation_exchange_id
```

### Example 7: Upload Document to IPFS

```python
# Python example using IPFS service
from shared.services.ipfs_service import IPFSService

ipfs = IPFSService("http://localhost:5001", "http://localhost:8080")

# Upload document
with open("diploma.pdf", "rb") as f:
    result = await ipfs.add_file(
        file_data=f.read(),
        filename="diploma.pdf",
        mime_type="application/pdf"
    )

print(f"CID: {result['cid']}")
print(f"Gateway URL: {ipfs.get_gateway_url(result['cid'])}")

# Pin for persistence
await ipfs.pin_add(result['cid'])
```

---

## Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_issuer.py -v
pytest tests/test_verifier.py -v
pytest tests/test_ipfs.py -v

# Run with coverage report
pytest tests/ --cov=agents --cov=shared --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are already in use
lsof -i :8000  # Issuer API
lsof -i :8001  # Verifier API
lsof -i :5432  # PostgreSQL
lsof -i :9000  # Indy Ledger

# Kill processes using ports
kill -9 <PID>

# Remove old containers
docker-compose -f infrastructure/docker-compose.yml down -v

# Restart
bash infrastructure/scripts/start-system.sh
```

### Indy Network Issues

```bash
# Check von-network status
cd infrastructure/von-network
./manage status

# View logs
./manage logs

# Restart Indy network
./manage stop
./manage start --logs
```

### Database Connection Errors

```bash
# Check PostgreSQL logs
docker logs ssi-postgres

# Connect to database manually
docker exec -it ssi-postgres psql -U postgres -d wallet_db

# Verify tables exist
\dt

# Check database initialization
docker exec -it ssi-postgres psql -U postgres -c "SELECT * FROM audit_log;"
```

### IPFS Not Responding

```bash
# Check IPFS status
docker logs ssi-ipfs

# Verify IPFS API
curl -X POST http://localhost:5001/api/v0/id

# Restart IPFS
docker restart ssi-ipfs
```

### Agent Health Check Fails

```bash
# Check agent logs
docker logs ssi-issuer-agent
docker logs ssi-verifier-agent

# Verify ACA-Py admin API
curl -H "X-API-Key: issuer-api-key-change-me-in-production" \
  http://localhost:8030/status

# Check wallet initialization
docker exec -it ssi-postgres psql -U postgres -d wallet_db \
  -c "SELECT * FROM credential_metadata LIMIT 5;"
```

---

## Stopping the System

```bash
# Stop all services gracefully
bash infrastructure/scripts/stop-system.sh

# This will:
# 1. Stop Docker Compose services
# 2. Stop Indy network (von-network)
# 3. Clean up resources

# To also remove data volumes (⚠️ DESTRUCTIVE)
cd infrastructure
docker-compose down -v
```

---

## Development Workflow

### Local Development

```bash
# Install Python dependencies
cd agents/issuer
pip install -r requirements.txt

# Run issuer API locally
python -m uvicorn app:app --reload --port 8000

# In another terminal, run verifier API
cd agents/verifier
python -m uvicorn app:app --reload --port 8001
```

### Code Changes

```bash
# After making code changes, rebuild containers
cd infrastructure
docker-compose build

# Restart affected service
docker-compose restart issuer-api
docker-compose restart verifier-api
```

### View Logs

```bash
# Follow logs for all services
docker-compose -f infrastructure/docker-compose.yml logs -f

# Follow specific service
docker logs -f ssi-issuer-agent
docker logs -f ssi-verifier-agent
docker logs -f ssi-postgres
```

---

## Next Steps

### For Developers:
1. **Explore API Documentation**: http://localhost:8000/docs
2. **Run Tests**: `pytest tests/ -v`
3. **Read Implementation Guide**: See `IMPLEMENTATION_STATUS.md`
4. **Start Sprint 3**: Begin mobile wallet implementation

### For Mobile Wallet Development (Sprint 3):
1. Read: `frontend/mobile/MOBILE_WALLET_PLAN.md`
2. Initialize React Native project
3. Install Aries Credo SDK
4. Test connection with issuer/verifier

### For Production Deployment:
1. Update `.env` with production keys
2. Enable TLS/HTTPS
3. Configure firewall rules
4. Set up monitoring (Prometheus + Grafana)
5. Enable backup automation
6. Review `docs/SECURITY_GOVERNANCE.md`

---

## Support & Resources

- **Documentation**: See `/docs` directory
- **API Reference**: http://localhost:8000/docs (when running)
- **Hyperledger Aries**: https://github.com/hyperledger/aries-cloudagent-python
- **Hyperledger Indy**: https://github.com/hyperledger/indy-node
- **Aries Bifold**: https://github.com/hyperledger/aries-mobile-agent-react-native
- **IPFS**: https://docs.ipfs.tech/

---

## Success Checklist

- [ ] All services start without errors
- [ ] Can create DID on issuer agent
- [ ] Can create schema and credential definition
- [ ] Can create connection invitation
- [ ] Can issue credential (using mock holder)
- [ ] Can request and verify proof (using mock holder)
- [ ] IPFS can store and retrieve documents
- [ ] PostgreSQL stores wallet data
- [ ] All health checks pass
- [ ] Tests run successfully

**If all checks pass: System is ready for Sprint 3 (Mobile Wallet)!** 🎉

---

**Last Updated**: November 13, 2025  
**Version**: 1.0.0
