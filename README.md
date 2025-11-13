# 🔐 Decentralized Digital Identity & Credential Vault

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Hyperledger](https://img.shields.io/badge/Hyperledger-Aries%20%7C%20Indy-red.svg)](https://www.hyperledger.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)

A production-ready **Self-Sovereign Identity (SSI)** system built on Hyperledger Indy and Aries, enabling users to own and control their digital identities and credentials with zero-knowledge proof privacy.

## 🎯 Project Vision

Empower individuals with complete ownership and control of their digital identities, eliminating reliance on centralized authorities while ensuring privacy through selective disclosure and zero-knowledge proofs.

## ✨ Key Features

- 🆔 **Self-Sovereign Identity**: Users control their own DIDs and credentials
- 🔒 **Zero-Knowledge Proofs**: Prove facts without revealing underlying data
- 🎯 **Selective Disclosure**: Share only necessary attributes
- 🌐 **Decentralized Storage**: IPFS integration for documents
- 🔗 **W3C Standards Compliant**: DIDs and Verifiable Credentials
- 🚫 **Revocation Support**: Real-time credential status checking
- 🔐 **Military-Grade Cryptography**: Ed25519, AES-256, ChaCha20-Poly1305
- 🌐 **Web-Based Wallet**: React application with browser-native security

## 🚀 Quick Start

Get up and running in 5 minutes:

```bash
# Clone repository
git clone https://github.com/deveshyaara/CryptLocker_Jovian786.git
cd CryptLocker_Jovian786

# Run automated setup
./scripts/setup.sh

# Verify installation
./scripts/check_services.sh
```

**See [QUICKSTART.md](./QUICKSTART.md) for detailed quick start guide.**

## 📋 Prerequisites

- **Docker** 20.10+ and Docker Compose 2.0+
- **Python** 3.11+
- **Node.js** 18+ (for frontend)
- **8GB RAM** minimum (16GB recommended)
- **20GB** disk space

## 📚 Documentation

### Getting Started
- [📖 Setup Guide](./docs/SETUP.md) - Complete installation instructions
- [⚡ Quick Start](./QUICKSTART.md) - 5-minute setup
- [📘 Project Overview](./PROJECT_OVERVIEW.md) - Architecture and design

### Architecture & Design
- [🏗️ Architecture](./docs/architecture/) - System design and components
- [💾 Data Models](./docs/DATA_MODELS.md) - Schemas and structures
- [🔧 Technology Stack](./docs/TECH_STACK.md) - Tools and libraries
- [📊 MVP Sprint Plan](./docs/MVP_SPRINT_PLAN.md) - 24-hour development timeline

### Development
- [👨‍💻 Development Rules](./DEVELOPMENT_RULES.md) - Coding standards and guidelines
- [🔒 Security & Governance](./docs/SECURITY_GOVERNANCE.md) - Security protocols
- [🧪 Testing Guide](./docs/guides/testing.md) - Test strategies
- [🔌 API Reference](./docs/api/) - API documentation

## 🏗️ Architecture

```
┌─────────────┐         Issues VC          ┌─────────────┐
│   Issuer    │──────────────────────────▶│    Holder   │
│  (University)│                            │   (Alice)   │
└─────────────┘                            └─────────────┘
       │                                           │
       │ Publishes DID                Presents VP │
       │ & Schema                                  │
       ▼                                           ▼
┌──────────────────────────────────────────────────────┐
│         Hyperledger Indy Ledger (DID Registry)       │
└──────────────────────────────────────────────────────┘
       ▲                                           │
       │ Resolves DID                 Verifies VP │
       │                                           │
┌─────────────┐                            ┌─────────────┐
│  Verifier   │◀───────Verification────────│   IPFS      │
│ (Employer)  │         Request            │  (Docs)     │
└─────────────┘                            └─────────────┘
```

### Core Components

- **Hyperledger Indy**: Public DID registry and ledger
- **Hyperledger Aries**: Agent framework and DIDComm protocols
- **AnonCreds**: Zero-knowledge proof credentials
- **IPFS**: Decentralized document storage
- **PostgreSQL**: Local credential storage
- **React**: Web-based wallet interface

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Identity** | Hyperledger Indy | DID registry |
| **Agents** | Aries Cloud Agent (Python) | DIDComm protocols |
| **Storage** | Aries Askar | Secure wallet |
| **Privacy** | AnonCreds | Zero-knowledge proofs |
| **Files** | IPFS | Decentralized storage |
| **Database** | PostgreSQL 15 | Metadata storage |
| **Backend** | FastAPI (Python) | REST APIs |
| **Frontend** | React + TypeScript | Web wallet |
| **Crypto** | libsodium, Ed25519 | Cryptography |

## 📦 Project Structure

```
CryptLocker_Jovian786/
├── agents/                    # Agent implementations
│   ├── issuer/               # Issuer agent
│   ├── holder/               # Holder agent (wallet)
│   └── verifier/             # Verifier agent
├── docs/                     # Documentation
│   ├── architecture/         # System architecture
│   ├── api/                  # API specifications
│   ├── guides/               # How-to guides
│   └── governance/           # Governance framework
├── frontend/                 # Frontend applications
│   └── web/                 # Web-based wallet (React + TypeScript)
├── infrastructure/           # Infrastructure as code
│   ├── indy/                # Indy ledger setup
│   ├── database/            # Database scripts
│   └── ipfs/                # IPFS configuration
├── scripts/                 # Utility scripts
├── tests/                   # Test suites
├── docker-compose.yml       # Service orchestration
└── .env.example            # Environment template
```

## 🎬 Usage Examples

### Issue a Credential

```python
from aries_cloudagent.messaging.credential_definitions.util import CredDefQueryStringSchema

# Create credential offer
credential_offer = await agent.issue_credential(
    connection_id="abc-123",
    schema_id="Th7MpTa:2:degree:1.0",
    cred_def_id="Th7MpTa:3:CL:127:default",
    attributes={
        "name": "Alice Johnson",
        "degree": "Bachelor of Science",
        "university": "MIT",
        "graduation_date": "2025-05-20"
    }
)
```

### Request Proof with Selective Disclosure

```python
# Request only degree and university (not student ID or GPA)
proof_request = {
    "name": "Employment Verification",
    "requested_attributes": {
        "attr1": {"name": "degree"},
        "attr2": {"name": "university"}
    },
    "requested_predicates": {
        "pred1": {
            "name": "graduation_date",
            "p_type": ">=",
            "p_value": 20200101  # Graduated after 2020
        }
    }
}

presentation = await agent.request_proof(
    connection_id="xyz-789",
    proof_request=proof_request
)
```

### Verify Presentation

```python
# Verify cryptographic proof and check revocation
verification = await agent.verify_presentation(
    presentation_exchange_id="pres-456"
)

if verification.verified:
    print(f"Degree: {verification.revealed_attrs['degree']}")
    print(f"University: {verification.revealed_attrs['university']}")
    print(f"Graduated after 2020: {verification.predicates['pred1']}")
```

## 🔒 Security Features

- **Ed25519** signatures for DIDs and credentials
- **ChaCha20-Poly1305** encryption for wallet data
- **Zero-Knowledge Proofs** for selective disclosure
- **Pairwise DIDs** for unlinkability
- **Revocation registries** for credential lifecycle
- **Rate limiting** on all APIs
- **TLS 1.3** for all network communication
- **HSM support** for production key storage

## 🧪 Testing

```bash
# Run all tests
./scripts/run_tests.sh

# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# E2E tests
npm run test:e2e
```

## 📊 Development Roadmap

### ✅ Phase 1: Foundation (Complete)
- Project structure and documentation
- Development rules and standards
- Data models and schemas
- Security framework

### 🔄 Phase 2: Core Implementation (In Progress)
- [ ] Indy ledger integration
- [ ] Agent implementations (Issuer, Holder, Verifier)
- [ ] DIDComm protocols
- [ ] Credential lifecycle

### 📅 Phase 3: Advanced Features
- [ ] Zero-knowledge proof predicates
- [ ] IPFS document storage
- [ ] Revocation registries
- [ ] Mobile wallet

### 🚀 Phase 4: Production Ready
- [ ] Security audit
- [ ] Performance optimization
- [ ] Deployment automation
- [ ] Production monitoring

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](./CONTRIBUTING.md) before submitting PRs.

1. Fork the repository
2. Create a feature branch
3. Follow [Development Rules](./DEVELOPMENT_RULES.md)
4. Write tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hyperledger Foundation](https://www.hyperledger.org/)
- [W3C Credentials Community Group](https://www.w3.org/community/credentials/)
- [Decentralized Identity Foundation](https://identity.foundation/)
- [Sovrin Foundation](https://sovrin.org/)

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/deveshyaara/CryptLocker_Jovian786/issues)
- **Discussions**: [GitHub Discussions](https://github.com/deveshyaara/CryptLocker_Jovian786/discussions)
- **Email**: deveshyaara@example.com

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=deveshyaara/CryptLocker_Jovian786&type=Date)](https://star-history.com/#deveshyaara/CryptLocker_Jovian786&Date)

---

**Built with ❤️ for a decentralized future**