# 🏗️ Architecture Decision Record: Cloud-Hosted Wallet Model

**Date**: November 13, 2025  
**Status**: ✅ APPROVED  
**Decision**: Adopt **Cloud-Hosted Wallet Architecture** for production deployment

---

## 📋 Context

Initial project documentation contained conflicting information about the Holder Agent (Wallet) architecture:
- Some sections implied browser-embedded wallet (Aries Framework JavaScript in browser)
- Other sections showed cloud-hosted agent architecture
- User requirement: **Pure web-based application only**

## 🎯 Decision

We adopt the **Cloud-Hosted Wallet Model** where:

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     WEB BROWSER                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │         React Web Application                       │    │
│  │  (Thin Client - No Private Keys)                   │    │
│  │                                                      │    │
│  │  - Display credentials                              │    │
│  │  - QR code scanning                                 │    │
│  │  - User input/consent                               │    │
│  │  - IndexedDB for UI cache ONLY                      │    │
│  └────────────────┬───────────────────────────────────┘    │
└───────────────────┼──────────────────────────────────────────┘
                    │ HTTPS/WSS
                    │ (JWT/OAuth Authentication)
                    │
┌───────────────────▼──────────────────────────────────────────┐
│              BACKEND CLOUD SERVICES                          │
│                                                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │     Holder Agent (ACA-Py + FastAPI)              │       │
│  │  (Server-Side - Secure Key Storage)              │       │
│  │                                                   │       │
│  │  - Master private keys (encrypted)               │       │
│  │  - Credential storage                            │       │
│  │  - DIDComm protocol handler                      │       │
│  │  - Zero-knowledge proof generation               │       │
│  │  - Connection management                         │       │
│  └──────────────────────────────────────────────────┘       │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │PostgreSQL  │  │   IPFS     │  │Indy Ledger │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└──────────────────────────────────────────────────────────────┘
                    │
                    │ DIDComm
                    │
        ┌───────────┴──────────┐
        │                      │
   ┌────▼─────┐          ┌─────▼────┐
   │ Issuer   │          │ Verifier │
   │  Agent   │          │  Agent   │
   └──────────┘          └──────────┘
```

---

## ✅ Rationale

### Why Cloud-Hosted Wallet?

1. **Security**
   - ✅ Private keys never exposed to browser
   - ✅ Master secrets stored in secure server environment
   - ✅ No risk of XSS attacks stealing keys
   - ✅ Server-side hardware security module (HSM) support
   - ✅ Professional key management practices

2. **Compatibility**
   - ✅ Works with existing Hyperledger Aries infrastructure
   - ✅ Consistent with Issuer/Verifier architecture
   - ✅ Standard DIDComm protocol support
   - ✅ No browser compatibility issues

3. **User Experience**
   - ✅ Multi-device access (desktop, mobile browser, tablet)
   - ✅ No app installation required
   - ✅ Instant access from any device
   - ✅ Automatic backups and recovery
   - ✅ Seamless credential synchronization

4. **Operational**
   - ✅ Centralized monitoring and logging
   - ✅ Easy updates and patches
   - ✅ Professional support and maintenance
   - ✅ Compliance and audit capabilities

5. **Enterprise Ready**
   - ✅ Suitable for organizational wallets
   - ✅ Role-based access control
   - ✅ Multi-tenancy support
   - ✅ Integration with existing IAM systems

---

## 🔒 Security Model

### Authentication Flow

```
1. User opens web app → Login form
2. Web app sends credentials → Backend authentication service
3. Backend validates → Issues JWT token (short-lived: 15 min)
4. Web app stores JWT → localStorage (NOT private keys!)
5. All API calls → Include JWT in Authorization header
6. Backend validates JWT → Grants access to user's wallet
7. Session expires → Re-authentication required
```

### Key Storage Hierarchy

```
User Browser (React App)
├── JWT Token (15-minute expiry)
├── Session state (username, settings)
└── IndexedDB cache (credential metadata ONLY)
    ├── Credential IDs
    ├── Issuer names
    ├── Issuance dates
    └── Status indicators
    
Backend Server (Holder Agent)
├── Master private key (encrypted at rest)
├── Link secret (never leaves server)
├── Encrypted credentials
├── Connection records
└── DIDComm messages
```

### What Web App CAN Access

✅ Credential metadata (titles, issuers, dates)  
✅ Presentation requests  
✅ Connection invitations  
✅ Public DIDs  
✅ Verification results  

### What Web App CANNOT Access

❌ Master private keys  
❌ Link secrets  
❌ Full credential values (until presented)  
❌ Encryption keys  
❌ Wallet seed phrases  

---

## 📊 Component Responsibilities

### React Web Application (Frontend)

**Purpose**: User interface and presentation layer only

**Responsibilities**:
- Display credential list
- Scan QR codes for invitations
- Show presentation requests
- Collect user consent
- Display verification results
- Manage UI state

**Does NOT Handle**:
- Private key operations
- Cryptographic operations
- Credential encryption/decryption
- Zero-knowledge proof generation

**Technology**:
- React 18+ with TypeScript
- Material-UI or Tailwind CSS
- React Router for navigation
- Axios for HTTP requests
- html5-qrcode for QR scanning
- IndexedDB for UI cache only

### Holder Agent (Backend)

**Purpose**: Secure credential wallet with full SSI capabilities

**Responsibilities**:
- Generate and store DIDs
- Manage master private keys
- Handle DIDComm protocol
- Store encrypted credentials
- Generate zero-knowledge proofs
- Manage connections
- Process presentation requests

**Technology**:
- Hyperledger Aries Cloud Agent (ACA-Py) 0.11.0+
- FastAPI wrapper for REST API
- PostgreSQL for encrypted storage
- Integration with Indy ledger
- Integration with IPFS

**API Endpoints** (New - Sprint 3):
```
POST   /auth/register          # Create new wallet
POST   /auth/login             # Authenticate user
POST   /auth/refresh           # Refresh JWT
GET    /wallet/credentials     # List credentials
GET    /wallet/credentials/{id} # Get credential details
POST   /wallet/connections/accept # Accept invitation
GET    /wallet/presentations   # List proof requests
POST   /wallet/presentations/respond # Submit proof
```

---

## 🔄 User Workflows

### 1. Wallet Creation

```
User                    Web App                 Holder Agent
  │                       │                         │
  │ 1. Click "Register"   │                         │
  ├──────────────────────>│                         │
  │                       │                         │
  │                       │ 2. POST /auth/register  │
  │                       ├────────────────────────>│
  │                       │    (username, password) │
  │                       │                         │
  │                       │                         │ 3. Create wallet
  │                       │                         │    Generate DID
  │                       │                         │    Store encrypted
  │                       │                         │
  │                       │ 4. Return JWT + DID     │
  │                       │<────────────────────────┤
  │ 5. Show dashboard     │                         │
  │<──────────────────────┤                         │
```

### 2. Receiving Credential

```
User                    Web App                 Holder Agent              Issuer
  │                       │                         │                      │
  │ 1. Scan QR code       │                         │                      │
  ├──────────────────────>│                         │                      │
  │                       │                         │                      │
  │                       │ 2. POST /connections    │                      │
  │                       ├────────────────────────>│                      │
  │                       │    (invitation URL)     │                      │
  │                       │                         │                      │
  │                       │                         │ 3. DIDComm handshake │
  │                       │                         │<────────────────────>│
  │                       │                         │                      │
  │                       │                         │ 4. Credential offer  │
  │                       │                         │<─────────────────────┤
  │                       │                         │                      │
  │                       │ 5. Notification         │                      │
  │ 6. "New credential!"  │<────────────────────────┤                      │
  │<──────────────────────┤                         │                      │
  │                       │                         │                      │
  │ 7. Click "Accept"     │                         │                      │
  ├──────────────────────>│                         │                      │
  │                       │ 8. POST /credentials/   │                      │
  │                       │    accept               │                      │
  │                       ├────────────────────────>│                      │
  │                       │                         │                      │
  │                       │                         │ 9. Accept credential │
  │                       │                         ├─────────────────────>│
  │                       │                         │                      │
  │                       │                         │ 10. Store encrypted  │
  │                       │                         │                      │
  │                       │ 11. Success             │                      │
  │ 12. Show credential   │<────────────────────────┤                      │
  │<──────────────────────┤                         │                      │
```

### 3. Presenting Proof

```
User                    Web App                 Holder Agent           Verifier
  │                       │                         │                      │
  │                       │                         │ 1. Proof request     │
  │                       │                         │<─────────────────────┤
  │                       │                         │                      │
  │                       │ 2. Notification         │                      │
  │ 3. "Proof requested"  │<────────────────────────┤                      │
  │<──────────────────────┤                         │                      │
  │                       │                         │                      │
  │ 4. Review & consent   │                         │                      │
  ├──────────────────────>│                         │                      │
  │                       │                         │                      │
  │                       │ 5. POST /presentations/ │                      │
  │                       │    respond              │                      │
  │                       ├────────────────────────>│                      │
  │                       │                         │                      │
  │                       │                         │ 6. Generate ZKP      │
  │                       │                         │    (server-side)     │
  │                       │                         │                      │
  │                       │                         │ 7. Send presentation │
  │                       │                         ├─────────────────────>│
  │                       │                         │                      │
  │                       │ 8. Success              │                      │
  │ 9. "Verified!"        │<────────────────────────┤                      │
  │<──────────────────────┤                         │                      │
```

---

## 🚀 Implementation Plan (Revised)

### Sprint 3: Holder Agent Backend (6-8 hours)

**Focus**: Build secure cloud wallet service

1. **Agent Setup** (2 hours)
   - Deploy ACA-Py instance for holder
   - Configure wallet storage (PostgreSQL)
   - Set up DIDComm endpoints

2. **Authentication API** (2 hours)
   - User registration endpoint
   - JWT-based authentication
   - Session management
   - Password hashing (bcrypt)

3. **Wallet API** (4 hours)
   - Credential list endpoint
   - Credential details endpoint
   - Connection management
   - Presentation handling

**Deliverable**: Fully functional Holder Agent API

### Sprint 4: Web Frontend (10-12 hours)

**Focus**: Build user interface

1. **Project Setup** (2 hours)
   - Vite + React + TypeScript
   - UI framework (Material-UI)
   - Routing (React Router)
   - HTTP client (Axios)

2. **Authentication** (2 hours)
   - Login/Register forms
   - JWT token management
   - Protected routes
   - Auto-refresh logic

3. **Credential Management** (3 hours)
   - Credential list view
   - Credential details modal
   - QR code scanner
   - Connection acceptance

4. **Presentation Flow** (3 hours)
   - Proof request notification
   - Attribute selection UI
   - Consent confirmation
   - Result display

5. **Testing & Polish** (2 hours)
   - E2E testing
   - Responsive design
   - Error handling
   - Loading states

**Deliverable**: Complete web wallet interface

### Sprint 5: Production Hardening (4-6 hours)

**Focus**: Security, monitoring, and operational readiness

1. **Rate Limiting** (1 hour)
   - Implement on all APIs
   - 10 req/s for auth endpoints
   - 100 req/s for wallet endpoints

2. **Monitoring** (2 hours)
   - Prometheus metrics
   - Grafana dashboards
   - Alert rules

3. **Security Audit** (1 hour)
   - OWASP Top 10 review
   - Penetration testing
   - Dependency scanning

4. **Documentation** (1 hour)
   - API documentation
   - User guide
   - Deployment checklist

**Deliverable**: Production-ready system

---

## 📈 Benefits of This Approach

### For Users

✅ **No App Installation**: Access from any browser  
✅ **Multi-Device**: Same wallet on desktop, mobile, tablet  
✅ **Automatic Backups**: No risk of losing credentials  
✅ **Professional Security**: Enterprise-grade key management  
✅ **Easy Recovery**: Password reset flow available  

### For Developers

✅ **Simpler Frontend**: No crypto libraries in browser  
✅ **Standard Patterns**: REST API + JWT (familiar)  
✅ **Easier Testing**: Backend testable without browser  
✅ **Better Debugging**: Server-side logging  
✅ **Consistent Architecture**: Same as Issuer/Verifier  

### For Operations

✅ **Centralized Monitoring**: All services in one place  
✅ **Easy Updates**: No user app updates needed  
✅ **Professional Support**: Standard cloud deployment  
✅ **Compliance Ready**: Audit logs and controls  
✅ **Scalable**: Load balance multiple replicas  

---

## 🔐 Security Considerations

### Threats Mitigated

| Threat | Mitigation |
|--------|-----------|
| **Key theft from browser** | Keys never in browser, stored server-side only |
| **XSS attacks** | No sensitive data in browser localStorage |
| **Session hijacking** | Short-lived JWT (15 min), secure HTTP-only cookies |
| **Credential tampering** | Server-side cryptographic verification |
| **Replay attacks** | Nonce in API requests, timestamp validation |

### Additional Security Layers

1. **Multi-Factor Authentication** (Optional)
   - TOTP (Google Authenticator)
   - SMS verification
   - Email confirmation

2. **Device Fingerprinting**
   - Track known devices
   - Alert on new device login

3. **IP Whitelisting** (Enterprise)
   - Restrict access to corporate networks

4. **Audit Logging**
   - All wallet operations logged
   - User activity tracking
   - Anomaly detection

---

## ✅ Decision Validation

This architecture has been successfully deployed in production SSI systems:

- **BC Government** (Canada): Uses cloud-hosted ACA-Py agents
- **European Digital Identity Wallet**: Server-side key management
- **IBM Digital Credentials**: Cloud wallet architecture
- **Trinsic**: Managed cloud wallet service

---

## 📝 Next Actions

1. ✅ Update all documentation to reflect cloud-hosted model
2. ✅ Remove browser-embedded wallet references
3. ✅ Create detailed Holder Agent API specification
4. ✅ Update Sprint 3-4 implementation plan
5. ✅ Begin Holder Agent development

---

**Approved By**: Architecture Team  
**Date**: November 13, 2025  
**Status**: ✅ **ACTIVE - CANONICAL ARCHITECTURE**
