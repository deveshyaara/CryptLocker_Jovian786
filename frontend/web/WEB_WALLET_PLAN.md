# Web Wallet Foundation - React with Aries Framework JavaScript

## Overview
This directory will contain the web-based wallet application using React and Aries Framework JavaScript (AFJ) for SSI wallet functionality. Unlike mobile wallets, this web application runs in the browser with enhanced security through modern Web Crypto APIs.

## Architecture

### Technology Stack
- **React 18+**: Modern web application framework
- **TypeScript**: Type-safe development
- **Aries Framework JavaScript (AFJ)**: SSI wallet capabilities for web
- **React Router v6**: Client-side routing
- **Material-UI (MUI) or Tailwind CSS**: UI component library
- **Redux Toolkit**: State management
- **IndexedDB with encryption**: Secure browser-based storage
- **Web Crypto API**: Browser-native cryptography

### Security Features
- **Web Crypto API Integration**:
  - Browser-native key generation (Ed25519)
  - Secure key storage in IndexedDB with encryption
  - Hardware security module support (when available)
- **Session Management**: JWT-based authentication with secure cookies
- **AES-256-GCM Wallet Encryption**: All sensitive data encrypted at rest
- **BIP-39 Mnemonic Recovery**: 12/24-word phrase backup
- **End-to-End Encrypted DIDComm**: Secure peer-to-peer messaging
- **HTTPS-Only**: Force secure connections
- **Content Security Policy**: XSS protection

## Directory Structure (To Be Created)
```
frontend/web/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── src/
│   ├── components/               # Reusable UI components
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── QRScanner.tsx
│   │   ├── credentials/
│   │   │   ├── CredentialCard.tsx
│   │   │   ├── CredentialList.tsx
│   │   │   └── CredentialDetails.tsx
│   │   ├── connections/
│   │   │   ├── ConnectionList.tsx
│   │   │   └── InvitationModal.tsx
│   │   └── proofs/
│   │       ├── ProofRequest.tsx
│   │       └── AttributeSelector.tsx
│   ├── pages/                    # Application pages
│   │   ├── OnboardingPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── CredentialsPage.tsx
│   │   ├── ConnectionsPage.tsx
│   │   ├── ProofsPage.tsx
│   │   └── SettingsPage.tsx
│   ├── services/                 # Business logic services
│   │   ├── WalletService.ts      # Aries AFJ integration
│   │   ├── DIDService.ts         # DID management
│   │   ├── CredentialService.ts  # Credential operations
│   │   ├── ProofService.ts       # Proof operations
│   │   ├── StorageService.ts     # IndexedDB encryption
│   │   └── CryptoService.ts      # Web Crypto API wrapper
│   ├── store/                    # Redux store
│   │   ├── slices/
│   │   │   ├── walletSlice.ts
│   │   │   ├── credentialSlice.ts
│   │   │   └── connectionSlice.ts
│   │   └── store.ts
│   ├── hooks/                    # Custom React hooks
│   │   ├── useWallet.ts
│   │   ├── useCredentials.ts
│   │   └── useConnections.ts
│   ├── utils/                    # Utility functions
│   │   ├── encryption.ts
│   │   ├── validation.ts
│   │   └── formatters.ts
│   ├── types/                    # TypeScript types
│   │   ├── wallet.types.ts
│   │   ├── credential.types.ts
│   │   └── connection.types.ts
│   ├── config/                   # Configuration
│   │   └── agent.config.ts
│   ├── App.tsx                   # Root component
│   └── index.tsx                 # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts               # Vite bundler config
└── README.md
```

## Sprint 3-4: Web Wallet Implementation Plan

### Phase 1: Project Setup (Hours 0-4)
**Goal**: Establish React + TypeScript foundation with Aries Framework JavaScript

- [ ] Initialize React project with Vite
  ```bash
  npm create vite@latest cryptlocker-web -- --template react-ts
  ```
- [ ] Install Aries Framework JavaScript dependencies
  ```bash
  npm install @aries-framework/core @aries-framework/node
  npm install @aries-framework/askar @hyperledger/aries-askar-nodejs
  ```
- [ ] Set up Material-UI or Tailwind CSS
- [ ] Configure React Router v6
- [ ] Set up Redux Toolkit for state management
- [ ] Configure IndexedDB with encryption wrapper
- [ ] Create Web Crypto API service
- [ ] Set up environment configuration

**Deliverable**: Running React app with routing and UI framework

---

### Phase 2: Wallet Core (Hours 4-8)
**Goal**: Implement secure wallet initialization and key management

- [ ] **Wallet Initialization Service** (`WalletService.ts`):
  ```typescript
  class WalletService {
    async initialize(): Promise<Agent>
    async createWallet(password: string): Promise<Wallet>
    async unlockWallet(password: string): Promise<void>
    async lockWallet(): Promise<void>
    async exportWallet(): Promise<string>
    async importWallet(data: string, password: string): Promise<void>
  }
  ```

- [ ] **Crypto Service** (`CryptoService.ts`):
  ```typescript
  class CryptoService {
    async generateKey(): Promise<CryptoKey>
    async deriveKey(password: string, salt: Uint8Array): Promise<CryptoKey>
    async encrypt(data: string, key: CryptoKey): Promise<string>
    async decrypt(encryptedData: string, key: CryptoKey): Promise<string>
    async hash(data: string): Promise<string>
  }
  ```

- [ ] **Storage Service** (`StorageService.ts`):
  ```typescript
  class StorageService {
    async saveEncrypted(key: string, value: any, encryptionKey: CryptoKey): Promise<void>
    async loadEncrypted(key: string, encryptionKey: CryptoKey): Promise<any>
    async delete(key: string): Promise<void>
    async clear(): Promise<void>
  }
  ```

- [ ] Implement BIP-39 mnemonic generation (12/24 words)
- [ ] Create mnemonic backup/recovery flow
- [ ] Build secure session management
- [ ] Implement AES-256-GCM encryption for wallet data
- [ ] Create onboarding UI (create/import wallet)

**Deliverable**: Secure wallet creation and storage

---

### Phase 3: DID Management (Hours 8-12)
**Goal**: Enable DID generation and connection establishment

- [ ] **DID Service** (`DIDService.ts`):
  ```typescript
  class DIDService {
    async createDID(): Promise<DID>
    async resolveDID(did: string): Promise<DIDDocument>
    async listDIDs(): Promise<DID[]>
    async setPublicDID(did: string): Promise<void>
  }
  ```

- [ ] **Connection Service** (part of AFJ):
  - Create connection invitations
  - Receive and accept invitations
  - List active connections
  - Delete connections

- [ ] Build QR code scanner component (html5-qrcode)
  ```typescript
  const QRScanner: React.FC<{
    onScan: (invitationUrl: string) => void;
  }>
  ```

- [ ] Create connection invitation modal
- [ ] Build connections list UI
- [ ] Implement DIDComm message handling
- [ ] Add connection status indicators

**Deliverable**: Functional connection management

---

### Phase 4: Credential Management (Hours 12-16)
**Goal**: Receive, store, and display credentials

- [ ] **Credential Service** (`CredentialService.ts`):
  ```typescript
  class CredentialService {
    async receiveOffer(offer: CredentialOffer): Promise<void>
    async acceptOffer(credentialId: string): Promise<void>
    async rejectOffer(credentialId: string): Promise<void>
    async listCredentials(): Promise<Credential[]>
    async getCredential(id: string): Promise<Credential>
    async deleteCredential(id: string): Promise<void>
    async checkRevocationStatus(credentialId: string): Promise<boolean>
  }
  ```

- [ ] Build credential offer reception handler
- [ ] Create credential acceptance/rejection flow
- [ ] Implement encrypted credential storage in IndexedDB
- [ ] Design credentials list page with filtering
  - Filter by issuer, type, status
  - Search by attributes
  - Sort by date received

- [ ] Create credential detail view
  - Display all attributes
  - Show issuer information
  - Revocation status indicator
  - IPFS document link (if present)

- [ ] Add credential expiration warnings
- [ ] Implement revocation status checking (background job)

**Deliverable**: Complete credential lifecycle management

---

### Phase 5: Selective Disclosure & Proof Presentation (Hours 16-20)
**Goal**: Handle proof requests with zero-knowledge proofs

- [ ] **Proof Service** (`ProofService.ts`):
  ```typescript
  class ProofService {
    async receiveRequest(request: ProofRequest): Promise<void>
    async getMatchingCredentials(request: ProofRequest): Promise<Credential[]>
    async createPresentation(
      request: ProofRequest,
      selectedAttributes: Record<string, string>
    ): Promise<Presentation>
    async submitPresentation(presentationId: string): Promise<void>
    async rejectRequest(requestId: string): Promise<void>
  }
  ```

- [ ] Build proof request notification system
- [ ] Create attribute selection UI
  - Show requested attributes
  - Highlight optional vs required
  - Support predicate proofs (age >= 18)
  - Preview what will be revealed

- [ ] Implement zero-knowledge proof generation (via AFJ)
- [ ] Create presentation submission flow
- [ ] Add proof request history
- [ ] Implement consent confirmation modal

**Deliverable**: Privacy-preserving credential presentation

---

### Phase 6: UI/UX Polish & Security Hardening (Hours 20-24)
**Goal**: Production-ready user experience

- [ ] **Responsive Design**:
  - Desktop layout (1920x1080)
  - Tablet layout (768x1024)
  - Mobile layout (375x667)

- [ ] **Loading States**:
  - Skeleton screens for lists
  - Progress indicators for operations
  - Optimistic UI updates

- [ ] **Error Handling**:
  - User-friendly error messages
  - Retry mechanisms
  - Offline mode detection
  - Network error recovery

- [ ] **Accessibility**:
  - WCAG 2.1 AA compliance
  - Keyboard navigation
  - Screen reader support
  - High contrast mode

- [ ] **Settings Page**:
  - Wallet backup/export
  - Security settings (session timeout)
  - Theme selection (light/dark)
  - Language preferences
  - Delete wallet option

- [ ] **Security Enhancements**:
  - Implement CSP headers
  - Add rate limiting
  - Session timeout after inactivity
  - Secure clipboard operations
  - Anti-phishing warnings

- [ ] **Documentation**:
  - User guide
  - FAQ section
  - Troubleshooting

**Deliverable**: Production-ready web wallet

---

## Integration Points

### Aries Framework JavaScript Configuration
```typescript
import { Agent, InitConfig, WsOutboundTransport } from '@aries-framework/core'
import { AskarModule } from '@aries-framework/askar'
import { ariesAskar } from '@hyperledger/aries-askar-nodejs'

const config: InitConfig = {
  label: 'CryptLocker Web Wallet',
  walletConfig: {
    id: 'web-wallet',
    key: 'encryption-key-from-user-password',
    storage: {
      type: 'askar',
      config: {
        // IndexedDB storage for browser
      },
    },
  },
  endpoints: ['ws://localhost:3000'], // WebSocket for DIDComm
  autoAcceptConnections: false,
  autoAcceptCredentials: false,
  autoAcceptProofs: false,
}

const agent = new Agent({
  config,
  modules: {
    askar: new AskarModule({ ariesAskar }),
  },
})

agent.registerOutboundTransport(new WsOutboundTransport())
await agent.initialize()
```

### Web Crypto API Example
```typescript
class CryptoService {
  async generateEncryptionKey(password: string): Promise<CryptoKey> {
    // Derive key from password using PBKDF2
    const encoder = new TextEncoder()
    const passwordBuffer = encoder.encode(password)
    const salt = crypto.getRandomValues(new Uint8Array(16))
    
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      passwordBuffer,
      { name: 'PBKDF2' },
      false,
      ['deriveKey']
    )
    
    return crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt,
        iterations: 100000,
        hash: 'SHA-256',
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt']
    )
  }
  
  async encryptData(data: string, key: CryptoKey): Promise<string> {
    const encoder = new TextEncoder()
    const dataBuffer = encoder.encode(data)
    const iv = crypto.getRandomValues(new Uint8Array(12))
    
    const encrypted = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      dataBuffer
    )
    
    // Combine IV + encrypted data
    const result = new Uint8Array(iv.length + encrypted.byteLength)
    result.set(iv, 0)
    result.set(new Uint8Array(encrypted), iv.length)
    
    return btoa(String.fromCharCode(...result))
  }
  
  async decryptData(encryptedData: string, key: CryptoKey): Promise<string> {
    const data = Uint8Array.from(atob(encryptedData), c => c.charCodeAt(0))
    const iv = data.slice(0, 12)
    const encrypted = data.slice(12)
    
    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      key,
      encrypted
    )
    
    const decoder = new TextDecoder()
    return decoder.decode(decrypted)
  }
}
```

### IndexedDB Storage with Encryption
```typescript
import { openDB, DBSchema, IDBPDatabase } from 'idb'

interface WalletDB extends DBSchema {
  credentials: {
    key: string
    value: {
      id: string
      encryptedData: string
      metadata: {
        issuer: string
        type: string
        receivedAt: string
      }
    }
  }
  connections: {
    key: string
    value: {
      id: string
      encryptedData: string
      metadata: {
        alias: string
        state: string
        createdAt: string
      }
    }
  }
  wallet: {
    key: string
    value: {
      encryptedSeed: string
      salt: string
      createdAt: string
    }
  }
}

class StorageService {
  private db: IDBPDatabase<WalletDB> | null = null
  
  async initialize(): Promise<void> {
    this.db = await openDB<WalletDB>('cryptlocker-wallet', 1, {
      upgrade(db) {
        db.createObjectStore('credentials', { keyPath: 'id' })
        db.createObjectStore('connections', { keyPath: 'id' })
        db.createObjectStore('wallet')
      },
    })
  }
  
  async saveCredential(
    credential: any,
    encryptionKey: CryptoKey
  ): Promise<void> {
    const cryptoService = new CryptoService()
    const encryptedData = await cryptoService.encryptData(
      JSON.stringify(credential),
      encryptionKey
    )
    
    await this.db!.put('credentials', {
      id: credential.id,
      encryptedData,
      metadata: {
        issuer: credential.issuer,
        type: credential.type,
        receivedAt: new Date().toISOString(),
      },
    })
  }
  
  async loadCredential(
    id: string,
    encryptionKey: CryptoKey
  ): Promise<any> {
    const stored = await this.db!.get('credentials', id)
    if (!stored) return null
    
    const cryptoService = new CryptoService()
    const decryptedData = await cryptoService.decryptData(
      stored.encryptedData,
      encryptionKey
    )
    
    return JSON.parse(decryptedData)
  }
}
```

## Security Considerations

### Key Storage Strategy
1. **Master Key Derivation**:
   - User password → PBKDF2 (100,000 iterations) → Master Key
   - Master Key stored in memory only (cleared on logout)
   - All wallet data encrypted with Master Key

2. **Session Management**:
   - JWT tokens for API authentication
   - HTTP-only secure cookies
   - Session timeout after 15 minutes of inactivity
   - Automatic wallet lock on tab close

3. **Data Encryption**:
   - Credentials encrypted with AES-256-GCM
   - Private keys encrypted separately
   - Metadata stored in plaintext for filtering (non-sensitive)

### Recovery Mechanism
1. **BIP-39 Mnemonic**:
   - 12 or 24-word phrase
   - User writes down on paper (recommended)
   - Optional encrypted cloud backup

2. **Wallet Export**:
   - Export encrypted wallet file
   - Requires password to decrypt
   - Contains all credentials and connections

### Browser Security
1. **Content Security Policy**:
   ```html
   <meta http-equiv="Content-Security-Policy" 
         content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'">
   ```

2. **HTTPS Enforcement**:
   - Redirect HTTP to HTTPS
   - HSTS headers
   - Secure cookie flags

3. **XSS Protection**:
   - Input sanitization
   - Output encoding
   - CSP headers

## Deployment

### Development
```bash
npm run dev
# Runs on http://localhost:5173
```

### Production Build
```bash
npm run build
# Creates optimized bundle in dist/

# Serve with nginx or apache
```

### Docker Deployment
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Testing Strategy

### Unit Tests (Jest + React Testing Library)
```bash
npm run test
```
- Component rendering
- Business logic in services
- Crypto operations
- Storage operations

### Integration Tests
- Wallet initialization flow
- Connection establishment
- Credential acceptance
- Proof presentation

### E2E Tests (Playwright or Cypress)
- Complete user workflows
- Cross-browser compatibility
- Responsive design validation

### Security Tests
- Penetration testing
- Encryption validation
- Session management testing
- XSS/CSRF protection verification

## Next Steps

### To Begin Web Wallet Implementation:

1. **Initialize Project**:
   ```bash
   cd frontend/web
   npm create vite@latest . -- --template react-ts
   npm install
   ```

2. **Install Dependencies**:
   ```bash
   # Aries Framework JavaScript
   npm install @aries-framework/core @aries-framework/node
   npm install @aries-framework/askar @hyperledger/aries-askar-nodejs
   
   # UI Framework
   npm install @mui/material @emotion/react @emotion/styled
   # OR
   npm install -D tailwindcss postcss autoprefixer
   
   # Routing & State
   npm install react-router-dom @reduxjs/toolkit react-redux
   
   # Utilities
   npm install idb bip39 qrcode.react html5-qrcode
   
   # Development
   npm install -D @types/node
   ```

3. **Configure Agent**:
   - Create `src/config/agent.config.ts`
   - Set up Aries AFJ with Askar wallet
   - Configure WebSocket transport

4. **Build Core Services**:
   - Start with CryptoService
   - Then StorageService
   - Finally WalletService

## References

- [Aries Framework JavaScript Documentation](https://aries.js.org/)
- [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [React Best Practices](https://react.dev/learn)
- [Material-UI](https://mui.com/) or [Tailwind CSS](https://tailwindcss.com/)
- [BIP-39 Mnemonic](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)

---

**Status**: Foundation documented, ready for Sprint 3-4 implementation  
**Priority**: HIGH - Core user-facing component  
**Dependencies**: Issuer and Verifier agents must be operational first  
**Platform**: Web browser (Chrome, Firefox, Safari, Edge)

