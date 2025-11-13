# Quick Start Guide

## Get Started in 5 Minutes

### 1. Clone and Setup
```bash
git clone https://github.com/deveshyaara/CryptLocker_Jovian786.git
cd CryptLocker_Jovian786

# Run automated setup
./scripts/setup.sh
```

### 2. Verify Installation
```bash
./scripts/check_services.sh
```

Expected output:
```
✅ Indy Ledger: Running
✅ PostgreSQL: Connected
✅ IPFS: Working
✅ Issuer Agent: Running
✅ Holder Agent: Running
✅ Verifier Agent: Running
```

### 3. Issue Your First Credential

```bash
# Create a connection between Issuer and Holder
curl -X POST http://localhost:8030/connections/create-invitation \
  -H "X-API-Key: $API_KEY_ISSUER" | jq

# Copy the invitation and accept it as Holder
curl -X POST http://localhost:8031/connections/receive-invitation \
  -H "Content-Type: application/json" \
  -d '{"invitation": {...}}'

# Issue a credential
curl -X POST http://localhost:8030/credentials/issue \
  -H "X-API-Key: $API_KEY_ISSUER" \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "...",
    "schema_id": "...",
    "attributes": {
      "name": "Alice",
      "degree": "BSc Computer Science"
    }
  }'
```

### 4. Access Web Interfaces

- **Indy Ledger**: http://localhost:9000
- **Issuer API Docs**: http://localhost:8030/api/doc
- **IPFS Web UI**: http://localhost:5001/webui

### 5. Next Steps

- Read [Full Documentation](./docs/SETUP.md)
- Explore [API Reference](./docs/api/)
- Run [Test Suite](./scripts/run_tests.sh)
- Start [Frontend](./frontend/wallet-ui/)

## Common Commands

```bash
# View logs
docker-compose logs -f issuer-agent

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Clean restart
docker-compose down -v && ./scripts/setup.sh
```

## Troubleshooting

**Issue**: Services won't start
```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs
```

**Issue**: Can't connect to ledger
```bash
# Restart Indy ledger
docker-compose restart indy-pool

# Wait 30 seconds, then verify
curl http://localhost:9000/status
```

## Need Help?

- [Setup Guide](./docs/SETUP.md)
- [Development Guide](./docs/guides/development.md)
- [GitHub Issues](https://github.com/deveshyaara/CryptLocker_Jovian786/issues)
