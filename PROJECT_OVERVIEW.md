# 🔐 Decentralized Digital Identity & Credential Vault

## Project Vision
A Self-Sovereign Identity (SSI) framework empowering users with full ownership and control of their digital identities and credentials, eliminating reliance on centralized authorities.

## 📊 Project Status
- **Phase**: MVP Development
- **Timeline**: 24-hour sprint (November 13-14, 2025)
- **Development Start**: November 13, 2025
- **Target MVP Completion**: November 14, 2025

## 🎯 Core Objectives

### Primary Goals
1. **Self-Sovereign Identity (SSI)**: Users maintain complete control over their digital identities
2. **Decentralized Architecture**: No single point of failure or control
3. **Privacy-First Design**: Selective disclosure using Zero-Knowledge Proofs
4. **Interoperability**: Adherence to W3C DID/VC standards
5. **Security**: Military-grade cryptography and secure key management

### Technical Goals
- ✅ Blockchain-based DID Registry (Hyperledger Indy)
- ✅ Verifiable Credentials issuance and verification
- ✅ Selective disclosure with ZKPs
- ✅ Web-based wallet (React + TypeScript)
- ✅ Decentralized file storage (IPFS)
- ✅ Revocation and lifecycle management

## 🏗️ Architecture

### SSI Trust Triangle

```
         ┌─────────────┐
         │   Issuer    │
         │ (VC Creator)│
         └──────┬──────┘
                │
        Issues VC│
                │
                ▼
         ┌─────────────┐         Presents VP        ┌─────────────┐
         │    Holder   │─────────────────────────────▶│  Verifier   │
         │(User Wallet)│                              │ (VC Checker)│
         └─────────────┘                              └─────────────┘
                │                                            │
                │                                            │
                └────────────────┬───────────────────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │ Hyperledger Indy    │
                      │  (DID Registry)     │
                      └─────────────────────┘
```

### Actor Responsibilities

| Actor | Role | Technology |
|-------|------|------------|
| **Issuer** | Creates and digitally signs Verifiable Credentials | Hyperledger Aries Cloud Agent (Python) |
| **Holder** | Stores private keys and VCs, presents selective disclosures | React Web Wallet + Aries Framework JavaScript |
| **Verifier** | Requests and verifies cryptographic proofs | Hyperledger Aries Verification Agent |

## 🛠️ Technology Stack

### Core Components

| Component | Technology | Purpose | Justification |
|-----------|-----------|---------|---------------|
| **DID Registry** | Hyperledger Indy | Public DID storage, revocation registries | W3C DID-compliant, PBFT consensus, proven in production |
| **Agent Framework** | Hyperledger Aries | P2P communication, VC/VP protocols | DIDComm protocol support, multi-platform SDKs |
| **Cryptography** | AnonCreds + ZKPs | Privacy-preserving credentials | Selective disclosure, unlinkability |
| **Storage** | IPFS | Decentralized document storage | Content-addressed, tamper-proof, distributed |
| **Wallet Backend** | Aries Askar | Secure credential storage | Hardware security module support |
| **Communication** | DIDComm v2 | Encrypted P2P messaging | End-to-end encryption, forward secrecy |

### Development Stack

- **Backend**: Python 3.11+ (Aries Cloud Agent Python - ACA-Py)
- **Frontend**: React 18+ with TypeScript (web-based wallet)
- **Database**: PostgreSQL (wallet storage), Indy Ledger (DIDs)
- **Container**: Docker & Docker Compose
- **Testing**: pytest, Jest, Playwright (E2E)
- **CI/CD**: GitHub Actions

## 📋 MVP Feature Set

### Phase 1: Core Infrastructure (Hours 0-8)
- [ ] Hyperledger Indy ledger setup (local development pool)
- [ ] ACA-Py instances for Issuer, Holder, Verifier
- [ ] DID creation and registration
- [ ] Basic DIDComm connection protocol

### Phase 2: Credential Lifecycle (Hours 8-16)
- [ ] Credential schema definition and publishing
- [ ] VC issuance workflow
- [ ] Credential storage in wallet
- [ ] IPFS integration for document storage
- [ ] Revocation registry setup

### Phase 3: Verification & Privacy (Hours 16-20)
- [ ] ZKP-based selective disclosure
- [ ] Proof request/presentation protocol
- [ ] Verification workflow
- [ ] Revocation checking

### Phase 4: UI & Integration (Hours 20-24)
- [ ] Basic wallet UI (web-based MVP)
- [ ] Issuer dashboard
- [ ] Verifier interface
- [ ] End-to-end integration testing

## 🔒 Security Architecture

### Key Management
- **Private Keys**: Stored in secure enclave/TEE (production) or encrypted storage (MVP)
- **Key Derivation**: BIP39 mnemonic seed phrase (12/24 words)
- **Encryption**: ChaCha20-Poly1305 for wallet data
- **Signing**: Ed25519 for DIDs and VCs

### Privacy Features
- **Selective Disclosure**: ZKP-based attribute revelation
- **Pairwise DIDs**: Unique DIDs per relationship
- **Unlinkability**: Cannot correlate user across verifiers
- **Minimal Disclosure**: Prove facts without revealing data

### Network Security
- **DIDComm**: End-to-end encrypted messaging
- **TLS**: All HTTP communications
- **Revocation**: Real-time credential status checking
- **Governance**: Multi-sig approval for schema changes

## 📐 Data Models

### DID Document
```json
{
  "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
  "verificationMethod": [{
    "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-1",
    "type": "Ed25519VerificationKey2018",
    "controller": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
    "publicKeyBase58": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
  }],
  "authentication": ["did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-1"],
  "service": [{
    "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#agent",
    "type": "IndyAgent",
    "serviceEndpoint": "https://agent.example.com"
  }]
}
```

### Verifiable Credential
```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "id": "http://example.edu/credentials/3732",
  "type": ["VerifiableCredential", "UniversityDegreeCredential"],
  "issuer": "did:indy:sovrin:Th7MpTaRZVRYnPiabds81Y",
  "issuanceDate": "2025-11-13T00:00:00Z",
  "credentialSubject": {
    "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
    "degree": {
      "type": "BachelorDegree",
      "name": "Bachelor of Science in Computer Science",
      "university": "Example University"
    },
    "documentHash": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG"
  },
  "proof": {
    "type": "Ed25519Signature2018",
    "created": "2025-11-13T00:00:00Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:indy:sovrin:Th7MpTaRZVRYnPiabds81Y#keys-1",
    "jws": "eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..."
  }
}
```

## 🔄 Core Workflows

### 1. Identity Creation
```
User → Generate Keys → Create DID → Register on Indy Ledger → Store in Wallet
```

### 2. Credential Issuance
```
Issuer → Define Schema → Create VC → Sign with Private Key → Send via DIDComm → Holder Stores
```

### 3. Selective Disclosure
```
Verifier → Request Proof → Holder Generates ZKP → Send VP → Verifier Checks Signature & Revocation
```

### 4. Revocation
```
Issuer → Update Revocation Registry → Publish to Ledger → Verifiers Check Status
```

## 🎯 24-Hour Sprint Plan

### Sprint 1: Foundation (0-6 hours)
**Goal**: Development environment and basic DID operations

- Set up Indy ledger (von-network)
- Deploy 3x ACA-Py agents (Issuer, Holder, Verifier)
- Implement DID creation and registration
- Test basic DIDComm connections

**Deliverable**: Working DID creation and P2P connection

### Sprint 2: Credentials (6-12 hours)
**Goal**: Complete credential lifecycle

- Define credential schemas
- Implement VC issuance
- Build wallet storage layer
- Integrate IPFS for documents
- Create revocation registries

**Deliverable**: Issue and store credentials

### Sprint 3: Verification (12-18 hours)
**Goal**: Privacy-preserving verification

- Implement proof requests
- Build ZKP presentation logic
- Create verification workflows
- Add revocation checking

**Deliverable**: End-to-end verification flow

### Sprint 4: Integration (18-24 hours)
**Goal**: Complete MVP with UI

- Build web-based wallet UI
- Create issuer dashboard
- Develop verifier interface
- Integration testing
- Documentation

**Deliverable**: Functional MVP demo

## 📚 Documentation Structure

```
/docs
├── architecture/
│   ├── system-design.md
│   ├── security-model.md
│   └── data-flow.md
├── api/
│   ├── issuer-api.md
│   ├── holder-api.md
│   └── verifier-api.md
├── guides/
│   ├── setup.md
│   ├── development.md
│   └── deployment.md
└── governance/
    ├── framework.md
    └── schema-approval.md
```

## 🚀 Getting Started

See [SETUP.md](./docs/SETUP.md) for detailed setup instructions.

## 📝 Development Rules

See [DEVELOPMENT_RULES.md](./DEVELOPMENT_RULES.md) for coding standards and contribution guidelines.

## 🤝 Governance

This project follows a consortium governance model. See [GOVERNANCE.md](./docs/governance/framework.md).

## 📄 License

See [LICENSE](./LICENSE) file for details.

---

**Next Steps**: Review this overview and proceed to Sprint 1 setup.
