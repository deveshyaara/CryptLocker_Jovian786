# Web Wallet Foundation - React with Cloud-Hosted Holder Agent

## Architecture Decision: Cloud-Hosted Wallet Model

**Selected Architecture**: Cloud-Hosted Wallet (Recommended for Production)

### Why Cloud-Hosted?
1. **Security**: Private keys stored on secure server infrastructure, not in browser
2. **Reliability**: Professional backup, disaster recovery, and monitoring
3. **Maintainability**: Centralized updates, no browser compatibility issues
4. **Scalability**: Handle millions of users with load balancing
5. **Auditability**: Server-side logging and compliance tracking

### What This Means
- **Holder Agent**: Separate ACA-Py service (like Issuer/Verifier agents)
- **Web Frontend**: Thin client (React UI only, no private keys)
- **Authentication**: OAuth2/JWT for secure API access
- **Storage**: Private keys on cloud server, metadata cache in browser

---

## Overview
This directory contains the web-based wallet application using React as a thin client that communicates with a cloud-hosted Holder Agent (ACA-Py). The Holder Agent manages private keys, credentials, and cryptographic operations securely on the server side.

## Architecture

### Technology Stack
- **Frontend**: React 18+ with TypeScript (thin client)
- **Backend**: Holder Agent (Hyperledger Aries Cloud Agent Python)
- **API**: RESTful API for wallet operations (FastAPI wrapper)
- **Authentication**: OAuth2/JWT with refresh tokens
- **UI Framework**: Material-UI (MUI) or Tailwind CSS
- **State Management**: Redux Toolkit
- **Browser Storage**: IndexedDB (credential metadata cache only, NO private keys)
- **Transport**: HTTPS for API, WebSocket for real-time notifications

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     User's Browser                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  React Web UI (Thin Client)                           │  │
│  │  - Display credentials                                │  │
│  │  - Handle user interactions                           │  │
│  │  - Cache metadata in IndexedDB (non-sensitive)        │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│                    HTTPS + JWT                               │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Cloud Infrastructure                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Holder API (FastAPI)                                 │  │
│  │  - User authentication (OAuth2/JWT)                   │  │
│  │  - REST endpoints for wallet operations               │  │
│  │  - Session management                                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Holder Agent (ACA-Py)                                │  │
│  │  - Private key management (Ed25519)                   │  │
│  │  - Credential storage (encrypted PostgreSQL)          │  │
│  │  - DID operations                                     │  │
│  │  - Zero-knowledge proof generation                    │  │
│  │  - DIDComm messaging                                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                  │  │
│  │  - User accounts                                      │  │
│  │  - Encrypted wallets                                  │  │
│  │  - Encrypted credentials                              │  │
│  │  - Audit logs                                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Security Features
- **Server-Side Key Storage**: Private keys never leave secure server environment
- **OAuth2/JWT Authentication**: Secure user authentication with refresh tokens
- **Encrypted Database**: All sensitive data encrypted at rest (AES-256-GCM)
- **HTTPS Only**: Enforced TLS 1.3 for all communications
- **Rate Limiting**: DDoS protection and abuse prevention
- **Session Management**: 15-minute inactivity timeout, secure token refresh
- **Audit Logging**: All operations logged for compliance
- **RBAC**: Role-based access control for multi-tenant support
- **Content Security Policy**: XSS protection
- **CORS**: Restricted cross-origin requests

---

## Directory Structure

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
│   │   ├── RegisterPage.tsx      # New user registration
│   │   ├── LoginPage.tsx         # User login
│   │   ├── DashboardPage.tsx
│   │   ├── CredentialsPage.tsx
│   │   ├── ConnectionsPage.tsx
│   │   ├── ProofsPage.tsx
│   │   └── SettingsPage.tsx
│   ├── services/                 # API client services
│   │   ├── ApiClient.ts          # Axios wrapper with JWT handling
│   │   ├── AuthService.ts        # Login, logout, token refresh
│   │   ├── WalletService.ts      # Wallet API calls
│   │   ├── CredentialService.ts  # Credential API calls
│   │   ├── ProofService.ts       # Proof API calls
│   │   ├── ConnectionService.ts  # Connection API calls
│   │   └── CacheService.ts       # IndexedDB metadata cache
│   ├── store/                    # Redux store
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── walletSlice.ts
│   │   │   ├── credentialSlice.ts
│   │   │   └── connectionSlice.ts
│   │   └── store.ts
│   ├── hooks/                    # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useWallet.ts
│   │   ├── useCredentials.ts
│   │   └── useWebSocket.ts
│   ├── utils/                    # Utility functions
│   │   ├── validation.ts
│   │   ├── formatters.ts
│   │   └── errorHandlers.ts
│   ├── types/                    # TypeScript types
│   │   ├── auth.types.ts
│   │   ├── wallet.types.ts
│   │   ├── credential.types.ts
│   │   └── api.types.ts
│   ├── config/                   # Configuration
│   │   └── api.config.ts         # API endpoints
│   ├── App.tsx                   # Root component
│   └── index.tsx                 # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md

agents/holder/                     # NEW: Holder Agent backend
├── main.py                        # FastAPI application
├── services/
│   ├── auth_service.py            # User authentication
│   ├── wallet_service.py          # Wallet operations
│   ├── credential_service.py      # Credential management
│   ├── proof_service.py           # Proof operations
│   └── connection_service.py      # Connection management
├── models/
│   ├── user.py                    # User database model
│   ├── wallet.py                  # Wallet model
│   └── audit_log.py               # Audit logging
├── schemas/
│   ├── auth.py                    # Pydantic schemas for auth
│   ├── wallet.py
│   ├── credential.py
│   └── proof.py
├── dependencies.py                # JWT authentication dependency
├── config.py                      # Configuration
└── requirements.txt
```

---

## Sprint 3-4: Web Wallet Implementation Plan

### Phase 1: Backend - Holder Agent Setup (Hours 0-6)
**Goal**: Deploy Holder Agent as ACA-Py service with user management

#### Holder Agent Infrastructure
- [ ] Create `agents/holder/` directory structure
- [ ] Set up ACA-Py configuration for Holder Agent
  ```yaml
  # docker-compose addition
  holder-agent:
    image: bcgovimages/aries-cloudagent:py36-1.16-1_0.11.0
    command: >
      start
      --label "CryptLocker Holder"
      --inbound-transport http 0.0.0.0 8004 
      --outbound-transport http
      --admin 0.0.0.0 11004 --admin-insecure-mode
      --endpoint http://holder-agent:8004
      --genesis-url http://indy-ledger:9000/genesis
      --wallet-type askar
      --wallet-name holder_wallet
      --wallet-key encryption_key_here
      --auto-provision
      --log-level info
    ports:
      - "8004:8004"   # Inbound transport
      - "11004:11004" # Admin API
    volumes:
      - holder-wallets:/home/indy/.indy_client/wallet
    networks:
      - cryptlocker-network
  ```

#### User Authentication System
- [ ] **User Registration** (`services/auth_service.py`):
  ```python
  class AuthService:
      async def register_user(
          self, 
          username: str, 
          email: str, 
          password: str
      ) -> User:
          """Create new user with encrypted wallet"""
          # Hash password with bcrypt
          hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
          
          # Create user in database
          user = User(
              username=username,
              email=email,
              hashed_password=hashed_password
          )
          db.add(user)
          
          # Create dedicated wallet for user via ACA-Py
          wallet_response = await acapy_client.post("/multitenancy/wallet", {
              "wallet_name": f"user_{user.id}",
              "wallet_key": generate_wallet_key(),
              "label": f"{username}'s Wallet"
          })
          
          user.wallet_id = wallet_response["wallet_id"]
          user.wallet_token = wallet_response["token"]  # Encrypted in DB
          db.commit()
          
          return user
      
      async def login(
          self, 
          username: str, 
          password: str
      ) -> dict:
          """Authenticate user and return JWT tokens"""
          user = db.query(User).filter_by(username=username).first()
          if not user or not bcrypt.checkpw(password.encode(), user.hashed_password):
              raise AuthenticationError("Invalid credentials")
          
          # Generate JWT tokens
          access_token = create_access_token(user.id)  # 15 min expiry
          refresh_token = create_refresh_token(user.id)  # 7 day expiry
          
          return {
              "access_token": access_token,
              "refresh_token": refresh_token,
              "token_type": "bearer"
          }
  ```

#### Holder API Endpoints
- [ ] **Setup FastAPI** (`agents/holder/main.py`):
  ```python
  from fastapi import FastAPI, Depends, HTTPException
  from fastapi.security import OAuth2PasswordBearer
  
  app = FastAPI(title="CryptLocker Holder API")
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
  
  # Authentication endpoints
  @app.post("/auth/register")
  async def register(request: RegisterRequest):
      return await auth_service.register_user(
          request.username, 
          request.email, 
          request.password
      )
  
  @app.post("/auth/login")
  async def login(request: LoginRequest):
      return await auth_service.login(request.username, request.password)
  
  @app.post("/auth/refresh")
  async def refresh_token(refresh_token: str):
      return await auth_service.refresh_access_token(refresh_token)
  
  @app.post("/auth/logout")
  async def logout(token: str = Depends(oauth2_scheme)):
      return await auth_service.logout(token)
  
  # Wallet endpoints
  @app.get("/wallet/did")
  async def get_public_did(current_user: User = Depends(get_current_user)):
      return await wallet_service.get_public_did(current_user)
  
  @app.post("/wallet/did/create")
  async def create_did(current_user: User = Depends(get_current_user)):
      return await wallet_service.create_did(current_user)
  
  # Connection endpoints
  @app.get("/connections")
  async def list_connections(current_user: User = Depends(get_current_user)):
      return await connection_service.list_connections(current_user)
  
  @app.post("/connections/create-invitation")
  async def create_invitation(current_user: User = Depends(get_current_user)):
      return await connection_service.create_invitation(current_user)
  
  @app.post("/connections/receive-invitation")
  async def receive_invitation(
      invitation_url: str,
      current_user: User = Depends(get_current_user)
  ):
      return await connection_service.receive_invitation(invitation_url, current_user)
  
  # Credential endpoints
  @app.get("/credentials")
  async def list_credentials(current_user: User = Depends(get_current_user)):
      return await credential_service.list_credentials(current_user)
  
  @app.post("/credentials/accept-offer")
  async def accept_credential(
      credential_exchange_id: str,
      current_user: User = Depends(get_current_user)
  ):
      return await credential_service.accept_offer(credential_exchange_id, current_user)
  
  # Proof endpoints
  @app.get("/proofs/requests")
  async def list_proof_requests(current_user: User = Depends(get_current_user)):
      return await proof_service.list_requests(current_user)
  
  @app.post("/proofs/send-presentation")
  async def send_presentation(
      proof_request_id: str,
      selected_credentials: dict,
      current_user: User = Depends(get_current_user)
  ):
      return await proof_service.send_presentation(
          proof_request_id, 
          selected_credentials, 
          current_user
      )
  ```

#### Database Schema
- [ ] **User Table** (`models/user.py`):
  ```python
  class User(Base):
      __tablename__ = "users"
      
      id = Column(UUID, primary_key=True, default=uuid.uuid4)
      username = Column(String(50), unique=True, nullable=False)
      email = Column(String(255), unique=True, nullable=False)
      hashed_password = Column(String(255), nullable=False)
      wallet_id = Column(String(255))  # ACA-Py wallet ID
      wallet_token = Column(Text)  # Encrypted wallet access token
      is_active = Column(Boolean, default=True)
      created_at = Column(DateTime, default=datetime.utcnow)
      last_login = Column(DateTime)
  ```

- [ ] **Audit Log Table** (`models/audit_log.py`):
  ```python
  class AuditLog(Base):
      __tablename__ = "audit_logs"
      
      id = Column(UUID, primary_key=True, default=uuid.uuid4)
      user_id = Column(UUID, ForeignKey("users.id"))
      action = Column(String(100))  # "credential_received", "proof_sent", etc.
      resource_type = Column(String(50))
      resource_id = Column(String(255))
      details = Column(JSONB)
      ip_address = Column(String(45))
      user_agent = Column(Text)
      timestamp = Column(DateTime, default=datetime.utcnow)
  ```

**Deliverable**: Functional Holder Agent backend with authentication

---

### Phase 2: Frontend - Project Setup (Hours 6-10)
**Goal**: Initialize React app with API integration

- [ ] Initialize React project with Vite
  ```bash
  cd frontend/web
  npm create vite@latest . -- --template react-ts
  ```

- [ ] Install dependencies
  ```bash
  # UI Framework
  npm install @mui/material @emotion/react @emotion/styled
  
  # HTTP Client
  npm install axios
  
  # Routing & State
  npm install react-router-dom @reduxjs/toolkit react-redux
  
  # Utilities
  npm install idb qrcode.react html5-qrcode
  npm install jwt-decode
  
  # Development
  npm install -D @types/node
  ```

- [ ] **API Client Setup** (`services/ApiClient.ts`):
  ```typescript
  import axios, { AxiosInstance } from 'axios'
  import { refreshAccessToken } from './AuthService'
  
  class ApiClient {
    private client: AxiosInstance
    
    constructor() {
      this.client = axios.create({
        baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8004',
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      // Request interceptor - add JWT token
      this.client.interceptors.request.use(
        (config) => {
          const token = localStorage.getItem('access_token')
          if (token) {
            config.headers.Authorization = `Bearer ${token}`
          }
          return config
        },
        (error) => Promise.reject(error)
      )
      
      // Response interceptor - handle token refresh
      this.client.interceptors.response.use(
        (response) => response,
        async (error) => {
          const originalRequest = error.config
          
          if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            
            try {
              const newToken = await refreshAccessToken()
              localStorage.setItem('access_token', newToken)
              originalRequest.headers.Authorization = `Bearer ${newToken}`
              return this.client(originalRequest)
            } catch (refreshError) {
              // Redirect to login
              window.location.href = '/login'
              return Promise.reject(refreshError)
            }
          }
          
          return Promise.reject(error)
        }
      )
    }
    
    get<T>(url: string): Promise<T> {
      return this.client.get(url).then(res => res.data)
    }
    
    post<T>(url: string, data?: any): Promise<T> {
      return this.client.post(url, data).then(res => res.data)
    }
    
    put<T>(url: string, data?: any): Promise<T> {
      return this.client.put(url, data).then(res => res.data)
    }
    
    delete<T>(url: string): Promise<T> {
      return this.client.delete(url).then(res => res.data)
    }
  }
  
  export const apiClient = new ApiClient()
  ```

- [ ] **Authentication Service** (`services/AuthService.ts`):
  ```typescript
  import { apiClient } from './ApiClient'
  import { jwtDecode } from 'jwt-decode'
  
  export class AuthService {
    async register(username: string, email: string, password: string) {
      const response = await apiClient.post('/auth/register', {
        username,
        email,
        password,
      })
      return response
    }
    
    async login(username: string, password: string) {
      const response = await apiClient.post<{
        access_token: string
        refresh_token: string
      }>('/auth/login', { username, password })
      
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      return response
    }
    
    async logout() {
      const token = localStorage.getItem('access_token')
      if (token) {
        await apiClient.post('/auth/logout')
      }
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
    
    async refreshAccessToken(): Promise<string> {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) throw new Error('No refresh token')
      
      const response = await apiClient.post<{ access_token: string }>(
        '/auth/refresh',
        { refresh_token: refreshToken }
      )
      
      return response.access_token
    }
    
    isAuthenticated(): boolean {
      const token = localStorage.getItem('access_token')
      if (!token) return false
      
      try {
        const decoded: any = jwtDecode(token)
        return decoded.exp * 1000 > Date.now()
      } catch {
        return false
      }
    }
  }
  
  export const authService = new AuthService()
  ```

- [ ] **Credential Cache Service** (`services/CacheService.ts`):
  ```typescript
  import { openDB, DBSchema, IDBPDatabase } from 'idb'
  
  interface WalletCache extends DBSchema {
    credentials: {
      key: string
      value: {
        id: string
        schema_name: string
        attributes: Record<string, string>
        issuer_name: string
        issued_at: string
        // NO private keys, NO sensitive crypto material
      }
    }
  }
  
  class CacheService {
    private db: IDBPDatabase<WalletCache> | null = null
    
    async initialize() {
      this.db = await openDB<WalletCache>('wallet-cache', 1, {
        upgrade(db) {
          db.createObjectStore('credentials', { keyPath: 'id' })
        },
      })
    }
    
    async cacheCredential(credential: any) {
      await this.db!.put('credentials', {
        id: credential.id,
        schema_name: credential.schema_name,
        attributes: credential.attributes,
        issuer_name: credential.issuer_name,
        issued_at: credential.issued_at,
      })
    }
    
    async getCachedCredentials() {
      return await this.db!.getAll('credentials')
    }
    
    async clearCache() {
      await this.db!.clear('credentials')
    }
  }
  
  export const cacheService = new CacheService()
  ```

**Deliverable**: React app with API integration and authentication

---

### Phase 3: Frontend - Core UI Components (Hours 10-14)
**Goal**: Build main application pages and credential display

- [ ] **Login Page** (`pages/LoginPage.tsx`)
- [ ] **Registration Page** (`pages/RegisterPage.tsx`)
- [ ] **Dashboard** (`pages/DashboardPage.tsx`): Overview of credentials, connections, pending actions
- [ ] **Credentials Page** (`pages/CredentialsPage.tsx`): List and detail views
- [ ] **Connections Page** (`pages/ConnectionsPage.tsx`): Manage connections with QR scanner
- [ ] **Proof Requests Page** (`pages/ProofsPage.tsx`): Handle incoming proof requests

- [ ] **Credential Card Component** (`components/credentials/CredentialCard.tsx`):
  ```typescript
  interface CredentialCardProps {
    credential: {
      id: string
      schema_name: string
      attributes: Record<string, string>
      issuer_name: string
      issued_at: string
      revocation_status?: 'active' | 'revoked'
    }
  }
  
  export const CredentialCard: React.FC<CredentialCardProps> = ({ credential }) => {
    return (
      <Card>
        <CardHeader
          title={credential.schema_name}
          subheader={`Issued by ${credential.issuer_name}`}
        />
        <CardContent>
          {Object.entries(credential.attributes).map(([key, value]) => (
            <Typography key={key}>
              <strong>{key}:</strong> {value}
            </Typography>
          ))}
          <Chip 
            label={credential.revocation_status === 'revoked' ? 'Revoked' : 'Active'}
            color={credential.revocation_status === 'revoked' ? 'error' : 'success'}
          />
        </CardContent>
      </Card>
    )
  }
  ```

**Deliverable**: Functional UI for credential and connection management

---

### Phase 4: Real-Time Notifications (Hours 14-18)
**Goal**: Handle real-time updates for credential offers and proof requests

- [ ] **WebSocket Service** (`services/WebSocketService.ts`):
  ```typescript
  class WebSocketService {
    private ws: WebSocket | null = null
    private reconnectAttempts = 0
    private maxReconnectAttempts = 5
    
    connect(token: string) {
      const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8004/ws'
      this.ws = new WebSocket(`${wsUrl}?token=${token}`)
      
      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
      }
      
      this.ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        this.handleMessage(message)
      }
      
      this.ws.onclose = () => {
        this.reconnect(token)
      }
    }
    
    handleMessage(message: any) {
      switch (message.type) {
        case 'credential_offer':
          store.dispatch(addCredentialOffer(message.data))
          // Show notification
          break
        case 'proof_request':
          store.dispatch(addProofRequest(message.data))
          // Show notification
          break
        case 'connection_request':
          store.dispatch(addConnectionRequest(message.data))
          break
      }
    }
    
    reconnect(token: string) {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          this.reconnectAttempts++
          this.connect(token)
        }, 1000 * Math.pow(2, this.reconnectAttempts))
      }
    }
    
    disconnect() {
      this.ws?.close()
    }
  }
  
  export const wsService = new WebSocketService()
  ```

- [ ] Add notification system for:
  - Credential offers received
  - Proof requests received
  - Connection requests
  - Credential revocation alerts

**Deliverable**: Real-time notification system

---

### Phase 5: Security & UX Polish (Hours 18-24)
**Goal**: Production-ready security and user experience

#### Security Hardening
- [ ] Implement HTTPS enforcement
- [ ] Add Content Security Policy headers
- [ ] Rate limiting on login endpoint (prevent brute force)
- [ ] Session timeout after 15 minutes inactivity
- [ ] Secure token storage (HTTP-only cookies for refresh tokens)
- [ ] Input validation on all forms
- [ ] XSS protection (sanitize user inputs)

#### UX Enhancements
- [ ] Loading states for all async operations
- [ ] Error handling with user-friendly messages
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessibility (WCAG 2.1 AA)
- [ ] Dark mode support
- [ ] Tutorial/onboarding flow for new users
- [ ] Settings page (change password, 2FA, export audit log)

#### Testing
- [ ] Unit tests for services (Jest)
- [ ] Component tests (React Testing Library)
- [ ] E2E tests (Playwright)
- [ ] Security tests (OWASP Top 10)

**Deliverable**: Production-ready web wallet

---

## Security Considerations

### Authentication Flow
```
1. User enters username/password
2. Frontend sends POST /auth/login
3. Backend validates credentials
4. Backend returns:
   - access_token (JWT, 15 min expiry) → localStorage
   - refresh_token (JWT, 7 day expiry) → HTTP-only cookie
5. Frontend stores access_token in memory/localStorage
6. All API requests include: Authorization: Bearer <access_token>
7. When access_token expires (401 response):
   - Frontend sends refresh_token to POST /auth/refresh
   - Backend returns new access_token
   - Retry original request
```

### Data Storage Strategy
| Data Type | Storage Location | Encrypted? |
|-----------|------------------|------------|
| Private keys | Server (PostgreSQL) | Yes (AES-256-GCM) |
| Credentials | Server (PostgreSQL) | Yes |
| User passwords | Server (PostgreSQL) | Yes (bcrypt) |
| Access token | Browser (localStorage) | No (short-lived) |
| Refresh token | Browser (HTTP-only cookie) | No (HttpOnly, Secure, SameSite) |
| Credential metadata | Browser (IndexedDB cache) | No (non-sensitive) |

### Comparison: Cloud vs Browser Wallet

| Feature | Cloud-Hosted (This Plan) | Browser-Embedded (AFJ) |
|---------|--------------------------|------------------------|
| Private key location | Secure server | User's browser |
| Key backup/recovery | Professional disaster recovery | User responsible |
| Browser compatibility | Any browser (thin client) | Limited (WASM support) |
| Offline support | No | Yes (limited) |
| Security model | Server-side hardening | Browser security (risky) |
| Scalability | Load balanced, HA | Per-user device |
| Auditability | Centralized logging | Difficult |
| **Production Ready** | ✅ Yes | ⚠️ Higher risk |

---

## Deployment

### Docker Compose Addition
```yaml
holder-api:
  build: ./agents/holder
  command: uvicorn main:app --host 0.0.0.0 --port 8004
  ports:
    - "8004:8004"
  environment:
    - DATABASE_URL=postgresql://user:pass@postgres:5432/cryptlocker
    - ACAPY_ADMIN_URL=http://holder-agent:11004
    - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    - JWT_ALGORITHM=HS256
    - ACCESS_TOKEN_EXPIRE_MINUTES=15
    - REFRESH_TOKEN_EXPIRE_DAYS=7
  depends_on:
    - holder-agent
    - postgres
  networks:
    - cryptlocker-network

holder-agent:
  image: bcgovimages/aries-cloudagent:py36-1.16-1_0.11.0
  command: >
    start
    --label "CryptLocker Holder"
    --inbound-transport http 0.0.0.0 8005
    --outbound-transport http
    --admin 0.0.0.0 11005 --admin-insecure-mode
    --endpoint http://holder-agent:8005
    --genesis-url http://indy-ledger:9000/genesis
    --wallet-type askar
    --wallet-name holder_wallet
    --wallet-key ${HOLDER_WALLET_KEY}
    --auto-provision
    --log-level info
  ports:
    - "8005:8005"
    - "11005:11005"
  volumes:
    - holder-wallets:/home/indy/.indy_client/wallet
  networks:
    - cryptlocker-network

web-ui:
  build: ./frontend/web
  ports:
    - "5173:80"
  environment:
    - VITE_API_URL=http://localhost:8004
    - VITE_WS_URL=ws://localhost:8004/ws
  networks:
    - cryptlocker-network
```

---

## Next Steps

### To Begin Implementation:

1. **Create Holder Agent Backend**:
   ```bash
   mkdir -p agents/holder/{services,models,schemas}
   touch agents/holder/main.py
   touch agents/holder/requirements.txt
   ```

2. **Install Backend Dependencies**:
   ```bash
   # agents/holder/requirements.txt
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   python-jose[cryptography]==3.3.0
   passlib[bcrypt]==1.7.4
   python-multipart==0.0.6
   sqlalchemy==2.0.23
   psycopg2-binary==2.9.9
   asyncpg==0.29.0
   httpx==0.25.1
   ```

3. **Setup Frontend**:
   ```bash
   cd frontend/web
   npm create vite@latest . -- --template react-ts
   npm install
   ```

4. **Update Docker Compose**:
   - Add holder-agent service
   - Add holder-api service
   - Add web-ui service

---

**Status**: Architecture documented, ready for Sprint 3-4 implementation  
**Priority**: HIGH - Core user-facing component  
**Dependencies**: Issuer and Verifier agents operational (✅ Complete)  
**Model**: Cloud-Hosted Wallet (private keys on server, React thin client)  
**Security**: OAuth2/JWT authentication, encrypted database storage
