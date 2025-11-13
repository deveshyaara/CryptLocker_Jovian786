# Technology Stack & Dependencies

## Core Technology Decisions

### 1. Hyperledger Indy - DID Registry

**Version**: 1.16+  
**Purpose**: Decentralized identifier (DID) storage and public key registry  
**Repository**: https://github.com/hyperledger/indy-node

**Why Indy?**
- ✅ Purpose-built for identity use cases
- ✅ W3C DID Method compliant (`did:indy`)
- ✅ Proven in production (Sovrin Network, IDUnion)
- ✅ PBFT consensus (high throughput, low latency)
- ✅ Built-in revocation registries
- ✅ Zero-knowledge proof support (AnonCreds)

**Alternatives Considered**:
- ❌ Ethereum: High gas costs, not identity-focused
- ❌ ION (Bitcoin): Slower finality, different trust model
- ❌ Cheqd: Less mature ecosystem

**Installation**:
```bash
# Using von-network (local development)
git clone https://github.com/bcgov/von-network
cd von-network
./manage build
./manage start --logs
```

### 2. Hyperledger Aries - Agent Framework

**Version**: 0.11.0+ (ACA-Py)  
**Purpose**: DIDComm protocols, credential exchange, wallet management  
**Repository**: https://github.com/hyperledger/aries-cloudagent-python

**Why Aries?**
- ✅ Complete RFC implementation (DIDComm, Issue Credential, Present Proof)
- ✅ Multi-language support (Python, Go, .NET, JavaScript)
- ✅ Production-ready with active maintenance
- ✅ Mediator support for mobile agents
- ✅ Extensible plugin architecture

**Components**:
```yaml
Agent Framework:
  - ACA-Py (Aries Cloud Agent - Python): Backend agents
  - Aries Framework JavaScript: Web wallet
  - Aries Framework Go: High-performance services

Protocol Support:
  - RFC 0160: Connection Protocol
  - RFC 0036: Issue Credential Protocol V1
  - RFC 0037: Present Proof Protocol V1
  - RFC 0453: Issue Credential Protocol V2
  - RFC 0454: Present Proof Protocol V2
  - RFC 0023: DID Exchange Protocol
```

**Installation**:
```bash
# Python
pip install aries-cloudagent==0.11.0

# Or using Docker
docker pull bcgovimages/aries-cloudagent:py36-1.16-1_0.11.0
```

### 3. Aries Askar - Secure Storage

**Version**: 0.3.0+  
**Purpose**: Encrypted wallet storage with hardware security support  
**Repository**: https://github.com/hyperledger/aries-askar

**Why Askar?**
- ✅ Replaces deprecated Indy-SDK wallet
- ✅ Hardware security module (HSM) support
- ✅ Secure enclave integration (iOS/Android)
- ✅ SQLite/PostgreSQL backends
- ✅ Advanced key derivation (BIP39)

**Features**:
- ChaCha20-Poly1305 encryption
- Argon2id key derivation
- AES-GCM hardware acceleration
- Multi-tenancy support

### 4. AnonCreds - Privacy-Preserving Credentials

**Version**: 0.2.0+  
**Purpose**: Zero-knowledge proof credential format  
**Repository**: https://github.com/hyperledger/anoncreds-rs

**Why AnonCreds?**
- ✅ Selective disclosure (reveal only required attributes)
- ✅ Predicate proofs (prove age > 18 without revealing age)
- ✅ Unlinkability (verifiers cannot correlate presentations)
- ✅ Revocation with privacy preservation

**Cryptographic Primitives**:
- CL Signatures (Camenisch-Lysyanskaya)
- Pedersen Commitments
- Range Proofs
- Accumulated revocation

### 5. IPFS - Decentralized Storage

**Version**: 0.27.0+ (Kubo)  
**Purpose**: Store large files (documents, images) with content addressing  
**Repository**: https://github.com/ipfs/kubo

**Why IPFS?**
- ✅ Content-addressed (tamper-proof via CID)
- ✅ Distributed (no single point of failure)
- ✅ Deduplication (efficient storage)
- ✅ Pinning services available (Pinata, Infura)

**Integration Pattern**:
```
1. Upload document to IPFS → Get CID (QmXxx...)
2. Store CID in Verifiable Credential
3. Verifier fetches document using CID
4. Verify hash matches CID
```

**Installation**:
```bash
# Using Docker
docker run -d --name ipfs \
  -p 4001:4001 -p 5001:5001 -p 8080:8080 \
  ipfs/kubo:v0.27.0
```

## Backend Stack

### Programming Language: Python 3.11+

**Why Python?**
- ✅ Primary language for ACA-Py
- ✅ Rich Hyperledger ecosystem
- ✅ Excellent async support (asyncio)
- ✅ Type hints for safety

**Required Packages**:
```toml
[tool.poetry.dependencies]
python = "^3.11"
aries-cloudagent = "^0.11.0"
aries-askar = "^0.3.0"
anoncreds = "^0.2.0"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.0"
sqlalchemy = "^2.0"
alembic = "^1.12"
psycopg2-binary = "^2.9"
python-multipart = "^0.0.6"
python-jose = {extras = ["cryptography"], version = "^3.3"}
passlib = {extras = ["bcrypt"], version = "^1.7"}
httpx = "^0.25"
aiofiles = "^23.0"
python-dotenv = "^1.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4"
pytest-asyncio = "^0.21"
pytest-cov = "^4.1"
black = "^23.0"
isort = "^5.12"
mypy = "^1.7"
pylint = "^3.0"
pre-commit = "^3.5"
```

### Web Framework: FastAPI

**Why FastAPI?**
- ✅ High performance (comparable to Node.js)
- ✅ Automatic OpenAPI documentation
- ✅ Type validation with Pydantic
- ✅ Async/await support
- ✅ Dependency injection

**Example Usage**:
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI(title="SSI Issuer API", version="1.0.0")

class CredentialRequest(BaseModel):
    holder_did: str
    schema_id: str
    attributes: dict

@app.post("/credentials/issue")
async def issue_credential(
    request: CredentialRequest,
    agent: ACAClient = Depends(get_agent)
):
    credential = await agent.issue_credential(
        request.holder_did,
        request.schema_id,
        request.attributes
    )
    return {"credential_id": credential.id}
```

### Database: PostgreSQL 15+

**Why PostgreSQL?**
- ✅ ACID compliance
- ✅ JSONB support for flexible schemas
- ✅ Full-text search
- ✅ Native UUID type
- ✅ Excellent with SQLAlchemy

**Schema Design**:
```sql
-- DIDs table
CREATE TABLE dids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    did TEXT UNIQUE NOT NULL,
    verkey TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Credentials table
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id TEXT UNIQUE NOT NULL,
    holder_did TEXT NOT NULL,
    schema_id TEXT NOT NULL,
    credential_data JSONB NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (holder_did) REFERENCES dids(did),
    INDEX idx_holder_did (holder_did),
    INDEX idx_schema_id (schema_id),
    INDEX idx_revoked (revoked)
);
```

## Frontend Stack

### Framework: React 18 + TypeScript

**Why React?**
- ✅ Largest ecosystem
- ✅ Web-based for cross-platform compatibility
- ✅ Excellent tooling (Vite, bundlers)
- ✅ Strong typing with TypeScript
- ✅ Progressive Web App (PWA) capabilities

**Dependencies**:
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@aries-framework/core": "^0.4.0",
    "@aries-framework/react-hooks": "^0.4.0",
    "react-router-dom": "^6.20.0",
    "zustand": "^4.4.0",
    "react-query": "^3.39.0",
    "axios": "^1.6.0",
    "zod": "^3.22.0",
    "react-hook-form": "^7.48.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### Web Wallet Security: Web Crypto API + IndexedDB

**Why Web-based approach?**
- ✅ Cross-platform: Works on desktop and mobile browsers
- ✅ Browser-native security (Web Crypto API)
- ✅ No app store deployment
- ✅ Aries Framework JavaScript support
- ✅ Progressive Web App capabilities

**Key Technologies**:
```typescript
// Web Crypto API for key generation
const keyPair = await crypto.subtle.generateKey(
  {
    name: "Ed25519",
    namedCurve: "Ed25519"
  },
  true,
  ["sign", "verify"]
);

// IndexedDB for encrypted storage
import { openDB } from 'idb';
const db = await openDB('wallet-db', 1);

// Aries Framework JavaScript
import { Agent } from '@aries-framework/core';
import { AskarModule } from '@aries-framework/askar';
```

**Key Libraries**:
```json
{
  "dependencies": {
    "@aries-framework/core": "^0.4.0",
    "@aries-framework/node": "^0.4.0",
    "@aries-framework/askar": "^0.4.0",
    "idb": "^7.1.1",
    "html5-qrcode": "^2.3.8",
    "qrcode": "^1.5.3",
    "bip39": "^3.1.0"
  }
}
```

### UI Framework: Tailwind CSS + shadcn/ui

**Why Tailwind + shadcn?**
- ✅ Utility-first CSS (fast development)
- ✅ Accessible components (shadcn)
- ✅ Customizable design system
- ✅ No runtime overhead

## Cryptography Libraries

### Core: libsodium (via PyNaCl)

**Why libsodium?**
- ✅ Audited and battle-tested
- ✅ Misuse-resistant API
- ✅ Hardware acceleration
- ✅ Used by Signal, Tor

**Algorithms**:
```python
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

# Ed25519 signatures (DID signing)
signing_key = SigningKey.generate()
verify_key = signing_key.verify_key

# Curve25519 (DIDComm encryption)
from nacl.public import PrivateKey, Box
alice_private = PrivateKey.generate()
bob_private = PrivateKey.generate()

box = Box(alice_private, bob_private.public_key)
encrypted = box.encrypt(b"secret message")
```

### Zero-Knowledge Proofs: AnonCreds

**Proof Types**:
```python
# Attribute reveal (selective disclosure)
proof_request = {
    "requested_attributes": {
        "attr1": {"name": "degree"}  # Reveal degree
    },
    "requested_predicates": {
        "pred1": {
            "name": "age",
            "p_type": ">=",
            "p_value": 18  # Prove age >= 18 without revealing
        }
    }
}
```

## DevOps Stack

### Containerization: Docker + Docker Compose

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  indy-pool:
    image: bcgovimages/von-network:latest
    ports:
      - "9000:8000"
      - "9701-9708:9701-9708"
  
  issuer-agent:
    build: ./agents/issuer
    ports:
      - "8020:8020"
      - "8030:8030"
    environment:
      - GENESIS_URL=http://indy-pool:8000/genesis
    depends_on:
      - indy-pool
      - postgres
  
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ssi_vault
      POSTGRES_USER: ssi_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  ipfs:
    image: ipfs/kubo:v0.27.0
    ports:
      - "4001:4001"
      - "5001:5001"
      - "8080:8080"
    volumes:
      - ipfs_data:/data/ipfs

volumes:
  postgres_data:
  ipfs_data:
```

### CI/CD: GitHub Actions

**.github/workflows/ci.yml**:
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run tests
        run: poetry run pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run linters
        run: |
          poetry run black --check .
          poetry run isort --check .
          poetry run mypy .
          poetry run pylint agents/
```

## Monitoring & Logging

### Logging: Structured JSON Logs

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "credential_issued",
    credential_id="cred_123",
    holder_did="did:indy:...",
    schema_id="schema:degree:1.0",
    issuer="university-issuer"
)
```

### Metrics: Prometheus + Grafana

**Metrics to Track**:
- Credential issuance rate
- Verification success/failure rate
- DIDComm message latency
- Ledger transaction time
- Wallet query performance

## Security Tools

### Secrets Management: Environment Variables + Vault (Production)

**Development**:
```bash
# .env (never commit!)
WALLET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
API_KEY=$(openssl rand -hex 32)
```

**Production**:
```bash
# Use HashiCorp Vault or AWS Secrets Manager
vault kv get -field=wallet_key secret/ssi/issuer
```

### Dependency Scanning

```yaml
# .github/workflows/security.yml
- name: Run Safety check
  run: poetry run safety check

- name: Run Bandit
  run: poetry run bandit -r agents/

- name: Run Snyk
  uses: snyk/actions/python@master
```

## Version Matrix

| Component | Version | Compatibility |
|-----------|---------|---------------|
| Python | 3.11+ | Required |
| Indy Node | 1.16+ | ACA-Py 0.11.0+ |
| ACA-Py | 0.11.0+ | Askar 0.3.0+ |
| Aries Askar | 0.3.0+ | ACA-Py 0.11.0+ |
| AnonCreds | 0.2.0+ | ACA-Py 0.11.0+ |
| PostgreSQL | 15+ | SQLAlchemy 2.0+ |
| Node.js | 18+ | React 18+ |
| Docker | 20.10+ | Compose 2.0+ |

## Installation Timeline

**Estimated Setup Time**: 30-45 minutes

1. **Prerequisites** (10 min): Docker, Python, Node.js
2. **Indy Network** (5 min): von-network startup
3. **Agents** (10 min): ACA-Py installation
4. **Database** (5 min): PostgreSQL setup
5. **IPFS** (5 min): IPFS node startup
6. **Frontend** (5 min): npm install

## Next Steps

- ✅ Review technology stack
- 📦 Run setup script: `./scripts/setup.sh`
- 🧪 Verify installation: `./scripts/verify_setup.sh`
- 📖 Read [Development Guide](./guides/development.md)

---

Last Updated: November 13, 2025
