# 24-Hour MVP Sprint Plan

## Overview
This document breaks down the 24-hour development timeline into 4 focused sprints, each with clear deliverables and success criteria.

## Sprint Summary

| Sprint | Hours | Focus | Deliverable |
|--------|-------|-------|-------------|
| Sprint 1 | 0-6 | Infrastructure & DIDs | Working DID creation and P2P connections |
| Sprint 2 | 6-12 | Credential Lifecycle | Issue and store credentials with IPFS |
| Sprint 3 | 12-18 | Verification & ZKPs | End-to-end verification with selective disclosure |
| Sprint 4 | 18-24 | UI & Integration | Complete MVP with functional interfaces |

---

## Sprint 1: Foundation & DIDs (Hours 0-6)

### Goal
Set up development infrastructure and implement basic DID operations.

### Tasks

#### Task 1.1: Infrastructure Setup (90 minutes)
**Owner**: DevOps  
**Priority**: P0

- [ ] Install Docker, Docker Compose, Python 3.11, Node.js 18
- [ ] Clone and start von-network (local Indy ledger)
- [ ] Set up PostgreSQL database
- [ ] Start IPFS node
- [ ] Verify all services are running

**Acceptance Criteria**:
```bash
# All services healthy
curl http://localhost:9000/status  # Indy: ready
curl http://localhost:5432  # PostgreSQL: accepting connections
curl http://localhost:5001/api/v0/version  # IPFS: working
```

#### Task 1.2: Agent Initialization (120 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Create ACA-Py configuration for 3 agents (Issuer, Holder, Verifier)
- [ ] Initialize wallets using Aries Askar
- [ ] Register each agent's DID on Indy ledger
- [ ] Configure DIDComm endpoints

**Acceptance Criteria**:
```bash
# Each agent has a registered DID
curl http://localhost:8030/wallet/did/public
# Returns: {"result": {"did": "did:indy:...", "verkey": "..."}}
```

**Files to Create**:
```
agents/
├── issuer/
│   ├── config/agent_config.yml
│   ├── scripts/init_wallet.py
│   └── scripts/register_did.py
├── holder/
│   └── [same structure]
└── verifier/
    └── [same structure]
```

#### Task 1.3: DID Creation API (60 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Implement POST /dids endpoint
- [ ] Add DID resolution (GET /dids/{did})
- [ ] Store DID metadata in PostgreSQL
- [ ] Add API authentication

**API Specification**:
```yaml
POST /api/v1/dids:
  summary: Create a new DID
  requestBody:
    content:
      application/json:
        schema:
          type: object
          properties:
            seed:
              type: string
              description: Optional 32-byte seed (hex)
  responses:
    201:
      content:
        application/json:
          schema:
            type: object
            properties:
              did:
                type: string
                example: "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw"
              verkey:
                type: string
              metadata:
                type: object
```

#### Task 1.4: Connection Protocol (90 minutes)
**Owner**: Backend Team  
**Priority**: P1

- [ ] Implement DIDComm connection invitation
- [ ] Add connection request/response handlers
- [ ] Store connections in database
- [ ] Test Issuer ↔ Holder connection

**Acceptance Criteria**:
```python
# Issuer creates invitation
invitation = await issuer_agent.create_invitation()

# Holder accepts invitation
connection = await holder_agent.accept_invitation(invitation)

# Connection is active
assert connection.state == "active"
```

### Sprint 1 Deliverables
- ✅ All infrastructure services running
- ✅ 3 agents with registered DIDs
- ✅ DID creation and resolution API
- ✅ Working P2P connections via DIDComm

### Sprint 1 Testing
```bash
# Run integration tests
cd tests/integration
pytest test_infrastructure.py
pytest test_did_operations.py
pytest test_connections.py
```

---

## Sprint 2: Credential Lifecycle (Hours 6-12)

### Goal
Implement complete credential issuance, storage, and IPFS integration.

### Tasks

#### Task 2.1: Schema Definition (60 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Create credential schema model
- [ ] Implement POST /schemas endpoint
- [ ] Publish schema to Indy ledger
- [ ] Add schema validation

**Schema Example**:
```json
{
  "name": "university-degree",
  "version": "1.0",
  "attributes": [
    "student_name",
    "degree_type",
    "major",
    "university",
    "graduation_date",
    "gpa",
    "student_id"
  ]
}
```

#### Task 2.2: Credential Definition (60 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Create credential definition from schema
- [ ] Publish cred_def to Indy ledger
- [ ] Store cred_def metadata
- [ ] Link cred_def to issuer DID

**Acceptance Criteria**:
```bash
# Schema and cred_def published
curl http://localhost:8030/schemas
curl http://localhost:8030/credential-definitions
```

#### Task 2.3: IPFS Integration (90 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Create IPFS client wrapper
- [ ] Implement file upload with encryption
- [ ] Generate and verify CIDs
- [ ] Add CID to credential metadata

**Implementation**:
```python
from ipfs_client import IPFSClient

class DocumentService:
    async def upload_document(self, file_data: bytes) -> str:
        """Upload document to IPFS and return CID."""
        # Optionally encrypt before upload
        encrypted_data = self.encrypt(file_data)
        
        # Upload to IPFS
        cid = await self.ipfs.add(encrypted_data)
        
        # Pin to ensure availability
        await self.ipfs.pin(cid)
        
        return cid
    
    async def fetch_document(self, cid: str) -> bytes:
        """Fetch document from IPFS using CID."""
        encrypted_data = await self.ipfs.cat(cid)
        return self.decrypt(encrypted_data)
```

#### Task 2.4: Credential Issuance (120 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Implement Issue Credential Protocol V2
- [ ] Create credential offer
- [ ] Sign credential with issuer's private key
- [ ] Send credential via DIDComm
- [ ] Store issued credential metadata

**Workflow**:
```
1. Issuer creates credential offer
2. Holder accepts offer (auto or manual)
3. Issuer signs and issues credential
4. Holder stores in wallet
5. Both parties store credential metadata
```

**API**:
```yaml
POST /api/v1/credentials/issue:
  requestBody:
    content:
      application/json:
        schema:
          type: object
          properties:
            connection_id:
              type: string
            schema_id:
              type: string
            attributes:
              type: object
            document_file:
              type: string
              format: binary
              description: Optional large file (stored in IPFS)
```

#### Task 2.5: Wallet Storage (60 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Implement credential storage in Askar wallet
- [ ] Add credential search/filter
- [ ] Implement GET /credentials endpoint
- [ ] Add credential metadata to PostgreSQL

**Data Model**:
```python
class StoredCredential:
    id: UUID
    holder_did: str
    credential_id: str  # Indy credential ID
    schema_id: str
    cred_def_id: str
    attributes: dict  # Encrypted
    ipfs_cid: Optional[str]
    revocation_reg_id: Optional[str]
    revocation_index: Optional[int]
    created_at: datetime
    revoked: bool = False
```

#### Task 2.6: Revocation Registry (90 minutes)
**Owner**: Backend Team  
**Priority**: P1

- [ ] Create revocation registry definition
- [ ] Publish to Indy ledger
- [ ] Implement credential revocation
- [ ] Add revocation status endpoint

**Implementation**:
```python
async def revoke_credential(
    self,
    credential_id: str,
    reason: str
) -> None:
    """Revoke a credential and update registry."""
    # Get credential details
    cred = await self.get_credential(credential_id)
    
    # Update revocation registry on ledger
    await self.ledger.revoke_credential(
        cred.revocation_reg_id,
        cred.revocation_index
    )
    
    # Mark as revoked in database
    await self.db.update_credential(
        credential_id,
        revoked=True,
        revoked_at=datetime.now(),
        revocation_reason=reason
    )
```

### Sprint 2 Deliverables
- ✅ Schema and cred_def creation
- ✅ IPFS document storage
- ✅ Complete credential issuance flow
- ✅ Wallet storage with search
- ✅ Revocation registry

### Sprint 2 Testing
```bash
pytest tests/integration/test_schemas.py
pytest tests/integration/test_credential_issuance.py
pytest tests/integration/test_ipfs.py
pytest tests/integration/test_revocation.py
```

---

## Sprint 3: Verification & ZKPs (Hours 12-18)

### Goal
Implement privacy-preserving verification with selective disclosure.

### Tasks

#### Task 3.1: Proof Request Definition (60 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Define proof request schema
- [ ] Implement attribute requests
- [ ] Implement predicate proofs
- [ ] Add restrictions (issuer, schema)

**Proof Request Example**:
```json
{
  "name": "Degree Verification",
  "version": "1.0",
  "requested_attributes": {
    "attr1_referent": {
      "name": "degree_type",
      "restrictions": [{
        "schema_id": "schema:university-degree:1.0",
        "issuer_did": "did:indy:sovrin:ABC123"
      }]
    },
    "attr2_referent": {
      "name": "university"
    }
  },
  "requested_predicates": {
    "pred1_referent": {
      "name": "graduation_date",
      "p_type": ">=",
      "p_value": 20200101,
      "restrictions": [{
        "schema_id": "schema:university-degree:1.0"
      }]
    }
  }
}
```

#### Task 3.2: Presentation Generation (120 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Implement Present Proof Protocol V2
- [ ] Generate ZKP from credentials
- [ ] Create verifiable presentation
- [ ] Send presentation via DIDComm

**Implementation**:
```python
async def create_presentation(
    self,
    proof_request: dict,
    credential_ids: List[str]
) -> dict:
    """Create ZKP presentation from credentials."""
    # Retrieve credentials from wallet
    credentials = await self.wallet.get_credentials(credential_ids)
    
    # Generate ZKP (AnonCreds)
    presentation = await self.anoncreds.create_presentation(
        proof_request=proof_request,
        credentials=credentials,
        self_attested={}  # Self-attested attributes
    )
    
    return presentation
```

#### Task 3.3: Proof Verification (90 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Implement presentation verification
- [ ] Verify cryptographic signatures
- [ ] Check revocation status
- [ ] Validate against proof request

**Verification Steps**:
```python
async def verify_presentation(
    self,
    presentation: dict,
    proof_request: dict
) -> VerificationResult:
    """Verify a presentation against proof request."""
    # 1. Verify cryptographic proof (ZKP)
    crypto_valid = await self.anoncreds.verify_presentation(
        presentation,
        proof_request
    )
    
    # 2. Check revocation status
    revoked = await self.check_revocation(presentation)
    
    # 3. Verify issuer DID is trusted
    issuer_trusted = await self.verify_issuer(
        presentation["issuer_did"]
    )
    
    # 4. Validate timestamps
    timestamps_valid = self.validate_timestamps(presentation)
    
    return VerificationResult(
        valid=all([crypto_valid, not revoked, issuer_trusted, timestamps_valid]),
        verified_attributes=self.extract_attributes(presentation),
        verified_predicates=self.extract_predicates(presentation),
        issuer_did=presentation["issuer_did"],
        errors=[]
    )
```

#### Task 3.4: Selective Disclosure (90 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Implement attribute selection UI flow
- [ ] Generate minimal disclosure presentation
- [ ] Verify only requested attributes revealed
- [ ] Add consent logging

**Example**:
```python
# Verifier requests: degree_type, university
# Holder's credential also contains: student_name, gpa, student_id

# Holder selects only requested attributes
selected_attributes = ["degree_type", "university"]

# Presentation reveals ONLY selected attributes
presentation = await create_presentation(
    proof_request=request,
    credentials=[credential_id],
    revealed_attributes=selected_attributes  # Not: student_name, gpa, student_id
)

# Verifier sees only: {"degree_type": "BSc", "university": "MIT"}
# Verifier CANNOT see: student_name, gpa, student_id
```

#### Task 3.5: Predicate Proofs (60 minutes)
**Owner**: Backend Team  
**Priority**: P1

- [ ] Implement age verification (>= 18) without revealing age
- [ ] Implement date range proofs
- [ ] Implement numeric comparisons (GPA >= 3.0)
- [ ] Test unlinkability

**Example**:
```python
# Prove age >= 18 without revealing actual age
proof_request = {
    "requested_predicates": {
        "age_check": {
            "name": "birth_date",
            "p_type": "<=",
            "p_value": 20051113  # Today - 18 years
        }
    }
}

# Holder generates ZKP
presentation = await create_presentation(proof_request, [id_credential])

# Verifier learns: "Yes, holder is 18+" but NOT actual birth date
result = await verify_presentation(presentation, proof_request)
assert result.predicates["age_check"]["satisfied"] == True
# Actual birth_date is NOT in result.verified_attributes
```

#### Task 3.6: Revocation Checking (60 minutes)
**Owner**: Backend Team  
**Priority**: P0

- [ ] Query revocation registry during verification
- [ ] Cache revocation status (with TTL)
- [ ] Handle revocation registry updates
- [ ] Add revocation timestamp to verification result

**Implementation**:
```python
async def check_revocation(
    self,
    presentation: dict
) -> bool:
    """Check if credential has been revoked."""
    rev_reg_id = presentation.get("revocation_reg_id")
    rev_index = presentation.get("revocation_index")
    
    if not rev_reg_id:
        return False  # No revocation support
    
    # Check cache first (TTL: 5 minutes)
    cached = await self.cache.get(f"rev:{rev_reg_id}:{rev_index}")
    if cached is not None:
        return cached
    
    # Query ledger
    revoked = await self.ledger.get_revocation_status(
        rev_reg_id,
        rev_index
    )
    
    # Cache result
    await self.cache.set(
        f"rev:{rev_reg_id}:{rev_index}",
        revoked,
        ttl=300
    )
    
    return revoked
```

### Sprint 3 Deliverables
- ✅ Proof request creation
- ✅ ZKP presentation generation
- ✅ Complete verification workflow
- ✅ Selective disclosure
- ✅ Predicate proofs (age, GPA)
- ✅ Revocation checking

### Sprint 3 Testing
```bash
pytest tests/integration/test_proof_requests.py
pytest tests/integration/test_presentations.py
pytest tests/integration/test_verification.py
pytest tests/integration/test_selective_disclosure.py
pytest tests/integration/test_predicates.py
```

---

## Sprint 4: UI & Integration (Hours 18-24)

### Goal
Build functional web interfaces and complete end-to-end testing.

### Tasks

#### Task 4.1: Wallet UI - Setup (60 minutes)
**Owner**: Frontend Team  
**Priority**: P0

- [ ] Initialize Vite + React + TypeScript project
- [ ] Set up Tailwind CSS
- [ ] Configure React Router
- [ ] Add state management (Zustand)
- [ ] Set up API client (Axios + React Query)

**Project Structure**:
```
frontend/wallet-ui/
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   ├── Credentials/
│   │   └── Presentations/
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Credentials.tsx
│   │   └── Settings.tsx
│   ├── services/
│   │   └── api.ts
│   ├── stores/
│   │   └── walletStore.ts
│   └── App.tsx
├── package.json
└── vite.config.ts
```

#### Task 4.2: Wallet UI - Core Features (120 minutes)
**Owner**: Frontend Team  
**Priority**: P0

- [ ] DID creation interface
- [ ] Credential list view
- [ ] Credential detail modal
- [ ] Connection management
- [ ] QR code scanner (for invitations)

**Key Components**:
```typescript
// components/CredentialCard.tsx
interface CredentialCardProps {
  credential: Credential;
  onView: (id: string) => void;
}

export const CredentialCard: React.FC<CredentialCardProps> = ({
  credential,
  onView
}) => {
  return (
    <div className="border rounded-lg p-4 shadow-sm">
      <h3 className="text-lg font-semibold">{credential.schema_name}</h3>
      <p className="text-gray-600">Issued by: {credential.issuer_name}</p>
      <p className="text-sm text-gray-500">
        {new Date(credential.issued_at).toLocaleDateString()}
      </p>
      <button onClick={() => onView(credential.id)}>
        View Details
      </button>
    </div>
  );
};
```

#### Task 4.3: Issuer Dashboard (90 minutes)
**Owner**: Frontend Team  
**Priority**: P0

- [ ] Schema creation form
- [ ] Credential issuance form
- [ ] Issued credentials list
- [ ] Revocation interface
- [ ] Connection invitations

**Issuance Form**:
```typescript
// pages/IssueCredential.tsx
export const IssueCredentialPage = () => {
  const [formData, setFormData] = useState({
    connection_id: '',
    schema_id: '',
    attributes: {},
    document: null as File | null
  });
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Upload document to IPFS if present
    let ipfsCid = null;
    if (formData.document) {
      ipfsCid = await uploadToIPFS(formData.document);
    }
    
    // Issue credential
    await issueCredential({
      ...formData,
      ipfs_cid: ipfsCid
    });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

#### Task 4.4: Verifier Interface (90 minutes)
**Owner**: Frontend Team  
**Priority**: P0

- [ ] Proof request builder
- [ ] Request presentation interface
- [ ] Verification result display
- [ ] Verification history

**Proof Request Builder**:
```typescript
// components/ProofRequestBuilder.tsx
export const ProofRequestBuilder = () => {
  const [attributes, setAttributes] = useState<AttributeRequest[]>([]);
  const [predicates, setPredicates] = useState<PredicateRequest[]>([]);
  
  const addAttribute = () => {
    setAttributes([...attributes, {
      name: '',
      restrictions: []
    }]);
  };
  
  const addPredicate = () => {
    setPredicates([...predicates, {
      name: '',
      p_type: '>=',
      p_value: 0,
      restrictions: []
    }]);
  };
  
  return (
    <div>
      <h2>Request Attributes</h2>
      {attributes.map((attr, i) => (
        <AttributeField key={i} {...attr} />
      ))}
      <button onClick={addAttribute}>Add Attribute</button>
      
      <h2>Request Predicates</h2>
      {predicates.map((pred, i) => (
        <PredicateField key={i} {...pred} />
      ))}
      <button onClick={addPredicate}>Add Predicate</button>
    </div>
  );
};
```

#### Task 4.5: Integration Testing (90 minutes)
**Owner**: QA Team  
**Priority**: P0

- [ ] End-to-end user flows
- [ ] API integration tests
- [ ] DIDComm message flow tests
- [ ] Error handling tests

**E2E Test Scenarios**:
```typescript
// tests/e2e/credential_flow.spec.ts
describe('Credential Issuance Flow', () => {
  it('should issue and verify a credential', async () => {
    // 1. Issuer creates connection invitation
    const invitation = await issuer.createInvitation();
    
    // 2. Holder accepts invitation
    await holder.acceptInvitation(invitation);
    
    // 3. Issuer issues credential
    const credential = await issuer.issueCredential({
      connection_id: invitation.connection_id,
      schema_id: 'schema:degree:1.0',
      attributes: {
        name: 'John Doe',
        degree: 'BSc',
        university: 'MIT'
      }
    });
    
    // 4. Holder receives credential
    const received = await holder.getCredential(credential.id);
    expect(received.attributes.degree).toBe('BSc');
    
    // 5. Verifier requests proof
    const proofRequest = await verifier.createProofRequest({
      requested_attributes: {
        attr1: { name: 'degree' }
      }
    });
    
    // 6. Holder creates presentation
    const presentation = await holder.createPresentation(
      proofRequest,
      [credential.id]
    );
    
    // 7. Verifier verifies presentation
    const result = await verifier.verify(presentation, proofRequest);
    expect(result.valid).toBe(true);
    expect(result.verified_attributes.degree).toBe('BSc');
  });
});
```

#### Task 4.6: Documentation & Demo (60 minutes)
**Owner**: Technical Writer  
**Priority**: P1

- [ ] Update API documentation
- [ ] Create user guide
- [ ] Record demo video
- [ ] Write deployment guide

### Sprint 4 Deliverables
- ✅ Functional wallet UI
- ✅ Issuer dashboard
- ✅ Verifier interface
- ✅ End-to-end tests passing
- ✅ Documentation complete

### Sprint 4 Testing
```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Integration tests
pytest tests/integration/

# Load tests
artillery run tests/load/credential_issuance.yml
```

---

## Success Criteria

### Functional Requirements
- [ ] User can create a DID
- [ ] Issuer can issue a credential
- [ ] Holder can store and view credentials
- [ ] Holder can create selective disclosure presentation
- [ ] Verifier can verify presentation
- [ ] System checks revocation status
- [ ] Documents stored in IPFS

### Non-Functional Requirements
- [ ] API response time < 500ms (p95)
- [ ] Zero security vulnerabilities (high/critical)
- [ ] 80%+ test coverage
- [ ] All services containerized
- [ ] Documentation complete

### Demo Scenarios

#### Scenario 1: University Degree
```
1. MIT (Issuer) issues degree credential to Alice (Holder)
2. Employer (Verifier) requests proof of degree
3. Alice selectively discloses: degree type, university
4. Alice does NOT reveal: student ID, GPA, graduation date
5. Employer verifies cryptographic proof
6. System checks credential not revoked
```

#### Scenario 2: Age Verification
```
1. Government (Issuer) issues ID credential to Bob
2. Bar (Verifier) requests proof: age >= 21
3. Bob proves age using predicate proof (ZKP)
4. Bob does NOT reveal actual birthdate
5. Bar verifies proof is valid
```

## Risk Management

### High-Risk Items
1. **Indy ledger stability**: Mitigation: Use von-network for development, Sovrin staging for testing
2. **DIDComm interoperability**: Mitigation: Extensive integration tests
3. **ZKP performance**: Mitigation: Profile and optimize, consider batching

### Blockers
- Indy network not starting → Switch to cloud-hosted ledger
- ACA-Py bugs → Downgrade to stable version (0.10.5)
- IPFS slow → Use local node, consider Pinata

## Team Coordination

### Roles
- **Backend Lead**: Agent development, protocols
- **Frontend Lead**: UI/UX, API integration
- **DevOps**: Infrastructure, CI/CD
- **QA**: Testing, verification
- **Tech Writer**: Documentation

### Communication
- **Standups**: Every 4 hours (0h, 4h, 8h, 12h, 16h, 20h)
- **Blocker resolution**: Immediately in Slack
- **Code review**: Required for all PRs
- **Demo prep**: Hour 23

### Tools
- **Git**: Feature branches, PR-based workflow
- **Slack**: Real-time communication
- **Jira**: Task tracking
- **GitHub Actions**: CI/CD

## Post-MVP Roadmap

### Week 2: Enhancements
- Mobile wallet (React Native)
- Advanced ZKP predicates
- Credential templates
- Bulk issuance

### Week 3-4: Production Readiness
- Security audit
- Performance optimization
- Monitoring and alerting
- Production deployment

### Month 2: Scale
- Multi-tenancy
- API rate limiting
- CDN for IPFS
- Backup and disaster recovery

---

**Last Updated**: November 13, 2025  
**Version**: 1.0
