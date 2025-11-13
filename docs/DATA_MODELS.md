# Data Models & Schemas

## Overview
This document defines all data structures used in the SSI system, including DID Documents, Verifiable Credentials, Verifiable Presentations, database schemas, and API models.

---

## 1. DID (Decentralized Identifier)

### DID Structure (W3C Compliant)
```
did:indy:sovrin:WRfXPg8dantKVubE3HX8pw
│   │     │       │
│   │     │       └─ Identifier (Base58 encoded public key)
│   │     └─ Namespace (sovrin, staging, local)
│   └─ Method (indy)
└─ Scheme (did)
```

### DID Document (JSON-LD)
```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
  "verificationMethod": [
    {
      "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-1",
      "type": "Ed25519VerificationKey2018",
      "controller": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
      "publicKeyBase58": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
    }
  ],
  "authentication": [
    "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-1"
  ],
  "assertionMethod": [
    "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-1"
  ],
  "keyAgreement": [
    {
      "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-2",
      "type": "X25519KeyAgreementKey2019",
      "controller": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
      "publicKeyBase58": "JhNWeSVLMYccCk7iopQW4guaSJTojqpMEELgSLhKwRr"
    }
  ],
  "service": [
    {
      "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#agent",
      "type": "IndyAgent",
      "serviceEndpoint": "https://agent.example.com",
      "recipientKeys": ["GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"],
      "routingKeys": []
    }
  ],
  "created": "2025-11-13T00:00:00Z",
  "updated": "2025-11-13T00:00:00Z"
}
```

### Python Model
```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class VerificationMethod:
    id: str
    type: str
    controller: str
    public_key_base58: str

@dataclass
class Service:
    id: str
    type: str
    service_endpoint: str
    recipient_keys: List[str]
    routing_keys: List[str]

@dataclass
class DIDDocument:
    context: List[str]
    id: str
    verification_method: List[VerificationMethod]
    authentication: List[str]
    assertion_method: List[str]
    key_agreement: List[VerificationMethod]
    service: List[Service]
    created: datetime
    updated: datetime
    
    def to_dict(self) -> dict:
        return {
            "@context": self.context,
            "id": self.id,
            "verificationMethod": [
                {
                    "id": vm.id,
                    "type": vm.type,
                    "controller": vm.controller,
                    "publicKeyBase58": vm.public_key_base58
                }
                for vm in self.verification_method
            ],
            # ... rest of fields
        }
```

---

## 2. Credential Schema

### Schema Definition (Indy Ledger)
```json
{
  "id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
  "name": "university-degree",
  "version": "1.0",
  "attrNames": [
    "student_name",
    "student_id",
    "degree_type",
    "major",
    "university",
    "graduation_date",
    "gpa",
    "honors"
  ],
  "seqNo": 127,
  "ver": "1.0"
}
```

### Credential Definition
```json
{
  "id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default",
  "schemaId": "127",
  "type": "CL",
  "tag": "default",
  "value": {
    "primary": {
      "n": "779...397",
      "s": "750..893",
      "r": {
        "student_name": "294...614",
        "student_id": "533...284",
        "degree_type": "635...769",
        "major": "234...897",
        "university": "443...191",
        "graduation_date": "794...946",
        "gpa": "324...556",
        "honors": "222...333",
        "master_secret": "521...922"
      },
      "rctxt": "774...977",
      "z": "632...005"
    },
    "revocation": {
      "g": "1 154...813",
      "g_dash": "1 2F7...AC7",
      "h": "1 131...990",
      "h0": "1 1AF...064",
      "h1": "1 242...A2D",
      "h2": "1 072...8A4",
      "htilde": "1 1D5...D99",
      "h_cap": "1 196...835",
      "u": "1 0C8...872",
      "pk": "1 0EE...2DC",
      "y": "1 1EE...A5F"
    }
  },
  "ver": "1.0"
}
```

### Python Model
```python
from typing import List, Dict
from pydantic import BaseModel, Field

class SchemaDefinition(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., regex=r"^\d+\.\d+$")
    attr_names: List[str] = Field(..., alias="attrNames", min_items=1)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "university-degree",
                "version": "1.0",
                "attrNames": ["student_name", "degree_type", "university"]
            }
        }

class CredentialDefinition(BaseModel):
    schema_id: str
    type: str = "CL"  # Camenisch-Lysyanskaya
    tag: str = "default"
    support_revocation: bool = True
```

---

## 3. Verifiable Credential

### Complete VC Example
```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1"
  ],
  "id": "http://university.example/credentials/3732",
  "type": ["VerifiableCredential", "UniversityDegreeCredential"],
  "issuer": {
    "id": "did:indy:sovrin:Th7MpTaRZVRYnPiabds81Y",
    "name": "Massachusetts Institute of Technology",
    "image": "https://mit.edu/logo.png"
  },
  "issuanceDate": "2025-11-13T19:23:24Z",
  "expirationDate": "2035-11-13T19:23:24Z",
  "credentialSubject": {
    "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
    "student_name": "Alice Johnson",
    "student_id": "MIT-2021-12345",
    "degree_type": "Bachelor of Science",
    "major": "Computer Science",
    "university": "Massachusetts Institute of Technology",
    "graduation_date": "2025-05-20",
    "gpa": "3.92",
    "honors": "Summa Cum Laude",
    "diploma_image_cid": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG"
  },
  "credentialSchema": {
    "id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
    "type": "IndyAnonCredsSchema2021"
  },
  "credentialStatus": {
    "id": "https://university.example/status/3732",
    "type": "RevocationList2020Status",
    "revocationListIndex": "94567",
    "revocationListCredential": "rev_reg_id:Th7MpTaRZVRYnPiabds81Y:4:..."
  },
  "proof": {
    "type": "CLSignature2019",
    "created": "2025-11-13T19:23:24Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:indy:sovrin:Th7MpTaRZVRYnPiabds81Y#keys-1",
    "signature": "eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19...",
    "primary_proof": {
      "eq_proof": {
        "revealed_attrs": {},
        "a_prime": "779...397",
        "e": "750...893",
        "v": "635...769",
        "m": {
          "master_secret": "294...614",
          "student_name": "533...284",
          "student_id": "635...769"
        },
        "m2": "324...556"
      },
      "ge_proofs": []
    },
    "non_revocation_proof": {
      "c_list": {...},
      "x_list": {...}
    }
  }
}
```

### Python Model
```python
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class Issuer(BaseModel):
    id: str  # DID
    name: str
    image: Optional[HttpUrl] = None

class CredentialSubject(BaseModel):
    id: str  # Holder DID
    # Dynamic attributes based on schema
    attributes: Dict[str, Any] = Field(..., alias="**")

class CredentialSchema(BaseModel):
    id: str
    type: str

class CredentialStatus(BaseModel):
    id: str
    type: str = "RevocationList2020Status"
    revocation_list_index: str
    revocation_list_credential: str

class Proof(BaseModel):
    type: str = "CLSignature2019"
    created: datetime
    proof_purpose: str = "assertionMethod"
    verification_method: str
    signature: str
    primary_proof: Dict[str, Any]
    non_revocation_proof: Optional[Dict[str, Any]] = None

class VerifiableCredential(BaseModel):
    context: List[str] = Field(..., alias="@context")
    id: str
    type: List[str]
    issuer: Issuer
    issuance_date: datetime = Field(..., alias="issuanceDate")
    expiration_date: Optional[datetime] = Field(None, alias="expirationDate")
    credential_subject: Dict[str, Any] = Field(..., alias="credentialSubject")
    credential_schema: CredentialSchema = Field(..., alias="credentialSchema")
    credential_status: Optional[CredentialStatus] = Field(None, alias="credentialStatus")
    proof: Proof
    
    class Config:
        allow_population_by_field_name = True
```

---

## 4. Verifiable Presentation

### Proof Request
```json
{
  "name": "Employment Verification",
  "version": "1.0",
  "nonce": "1234567890",
  "requested_attributes": {
    "attr1_referent": {
      "name": "degree_type",
      "restrictions": [
        {
          "schema_id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
          "issuer_did": "did:indy:sovrin:Th7MpTaRZVRYnPiabds81Y"
        }
      ]
    },
    "attr2_referent": {
      "name": "university"
    }
  },
  "requested_predicates": {
    "pred1_referent": {
      "name": "gpa",
      "p_type": ">=",
      "p_value": 3.5,
      "restrictions": [
        {
          "schema_id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0"
        }
      ]
    }
  },
  "non_revoked": {
    "from": 1699900000,
    "to": 1699999999
  }
}
```

### Verifiable Presentation
```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1"
  ],
  "type": ["VerifiablePresentation"],
  "verifiableCredential": [
    {
      "@context": ["https://www.w3.org/2018/credentials/v1"],
      "id": "http://university.example/credentials/3732",
      "type": ["VerifiableCredential", "UniversityDegreeCredential"],
      "issuer": "did:indy:sovrin:Th7MpTaRZVRYnPiabds81Y",
      "credentialSubject": {
        "id": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
        "degree_type": "Bachelor of Science",
        "university": "Massachusetts Institute of Technology"
      }
    }
  ],
  "proof": {
    "type": "AnonCredsPresentation2021",
    "created": "2025-11-13T20:00:00Z",
    "proofPurpose": "authentication",
    "verificationMethod": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw#keys-1",
    "challenge": "1234567890",
    "proofValue": {
      "requested_proof": {
        "revealed_attrs": {
          "attr1_referent": {
            "sub_proof_index": 0,
            "raw": "Bachelor of Science",
            "encoded": "27034640024117331033063128044004318218486816931520886405535659934417438781507"
          },
          "attr2_referent": {
            "sub_proof_index": 0,
            "raw": "Massachusetts Institute of Technology",
            "encoded": "..."
          }
        },
        "self_attested_attrs": {},
        "unrevealed_attrs": {},
        "predicates": {
          "pred1_referent": {
            "sub_proof_index": 0
          }
        }
      },
      "proof": {
        "proofs": [
          {
            "primary_proof": {
              "eq_proof": {...},
              "ge_proofs": [{...}]
            },
            "non_revoc_proof": {...}
          }
        ],
        "aggregated_proof": {
          "c_hash": "...",
          "c_list": [...]
        }
      },
      "identifiers": [
        {
          "schema_id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
          "cred_def_id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default",
          "rev_reg_id": "Th7MpTaRZVRYnPiabds81Y:4:...",
          "timestamp": 1699900000
        }
      ]
    }
  }
}
```

### Python Models
```python
class AttributeRestriction(BaseModel):
    schema_id: Optional[str] = None
    schema_name: Optional[str] = None
    schema_version: Optional[str] = None
    issuer_did: Optional[str] = None
    cred_def_id: Optional[str] = None

class RequestedAttribute(BaseModel):
    name: Optional[str] = None
    names: Optional[List[str]] = None
    restrictions: List[AttributeRestriction] = []
    non_revoked: Optional[Dict[str, int]] = None

class RequestedPredicate(BaseModel):
    name: str
    p_type: str = Field(..., regex=r"^(>=|>|<=|<)$")
    p_value: int
    restrictions: List[AttributeRestriction] = []
    non_revoked: Optional[Dict[str, int]] = None

class ProofRequest(BaseModel):
    name: str
    version: str = "1.0"
    nonce: str
    requested_attributes: Dict[str, RequestedAttribute]
    requested_predicates: Dict[str, RequestedPredicate]
    non_revoked: Optional[Dict[str, int]] = None

class RevealedAttribute(BaseModel):
    sub_proof_index: int
    raw: str
    encoded: str

class RequestedProof(BaseModel):
    revealed_attrs: Dict[str, RevealedAttribute]
    self_attested_attrs: Dict[str, str]
    unrevealed_attrs: Dict[str, Any]
    predicates: Dict[str, Dict[str, int]]

class VerifiablePresentation(BaseModel):
    context: List[str] = Field(..., alias="@context")
    type: List[str]
    verifiable_credential: List[Dict[str, Any]]
    proof: Dict[str, Any]
```

---

## 5. Database Schemas

### PostgreSQL Schema
```sql
-- DIDs table
CREATE TABLE dids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    did VARCHAR(255) UNIQUE NOT NULL,
    verkey VARCHAR(255) NOT NULL,
    method VARCHAR(50) NOT NULL DEFAULT 'indy',
    namespace VARCHAR(50) NOT NULL DEFAULT 'sovrin',
    metadata JSONB DEFAULT '{}',
    public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_did (did),
    INDEX idx_method_namespace (method, namespace)
);

-- Connections table
CREATE TABLE connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_id VARCHAR(255) UNIQUE NOT NULL,
    their_did VARCHAR(255) NOT NULL,
    my_did VARCHAR(255) NOT NULL,
    state VARCHAR(50) NOT NULL,  -- invitation, request, response, active, error
    their_label VARCHAR(255),
    their_role VARCHAR(50),
    invitation JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (my_did) REFERENCES dids(did),
    INDEX idx_connection_id (connection_id),
    INDEX idx_state (state),
    INDEX idx_their_did (their_did)
);

-- Schemas table
CREATE TABLE schemas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    schema_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    attributes TEXT[] NOT NULL,
    issuer_did VARCHAR(255) NOT NULL,
    seq_no INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (issuer_did) REFERENCES dids(did),
    INDEX idx_schema_id (schema_id),
    INDEX idx_name_version (name, version),
    INDEX idx_issuer_did (issuer_did)
);

-- Credential Definitions table
CREATE TABLE credential_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cred_def_id VARCHAR(255) UNIQUE NOT NULL,
    schema_id VARCHAR(255) NOT NULL,
    tag VARCHAR(100) DEFAULT 'default',
    type VARCHAR(50) DEFAULT 'CL',
    support_revocation BOOLEAN DEFAULT TRUE,
    revocation_registry_id VARCHAR(255),
    issuer_did VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (schema_id) REFERENCES schemas(schema_id),
    FOREIGN KEY (issuer_did) REFERENCES dids(did),
    INDEX idx_cred_def_id (cred_def_id),
    INDEX idx_schema_id (schema_id)
);

-- Credentials table
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id VARCHAR(255) UNIQUE NOT NULL,
    credential_exchange_id VARCHAR(255),
    holder_did VARCHAR(255) NOT NULL,
    issuer_did VARCHAR(255) NOT NULL,
    schema_id VARCHAR(255) NOT NULL,
    cred_def_id VARCHAR(255) NOT NULL,
    attributes JSONB NOT NULL,
    ipfs_cid VARCHAR(255),
    revocation_reg_id VARCHAR(255),
    revocation_index INTEGER,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP,
    revocation_reason TEXT,
    issued_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    
    FOREIGN KEY (holder_did) REFERENCES dids(did),
    FOREIGN KEY (issuer_did) REFERENCES dids(did),
    FOREIGN KEY (schema_id) REFERENCES schemas(schema_id),
    FOREIGN KEY (cred_def_id) REFERENCES credential_definitions(cred_def_id),
    INDEX idx_credential_id (credential_id),
    INDEX idx_holder_did (holder_did),
    INDEX idx_issuer_did (issuer_did),
    INDEX idx_schema_id (schema_id),
    INDEX idx_revoked (revoked),
    INDEX idx_ipfs_cid (ipfs_cid)
);

-- Presentations table
CREATE TABLE presentations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    presentation_exchange_id VARCHAR(255) UNIQUE NOT NULL,
    proof_request JSONB NOT NULL,
    presentation JSONB,
    verifier_did VARCHAR(255) NOT NULL,
    holder_did VARCHAR(255),
    verified BOOLEAN,
    verification_result JSONB,
    credential_ids UUID[],
    created_at TIMESTAMP DEFAULT NOW(),
    verified_at TIMESTAMP,
    
    FOREIGN KEY (verifier_did) REFERENCES dids(did),
    INDEX idx_presentation_exchange_id (presentation_exchange_id),
    INDEX idx_verifier_did (verifier_did),
    INDEX idx_holder_did (holder_did),
    INDEX idx_verified (verified)
);

-- Revocation Registries table
CREATE TABLE revocation_registries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rev_reg_id VARCHAR(255) UNIQUE NOT NULL,
    cred_def_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) DEFAULT 'CL_ACCUM',
    max_cred_num INTEGER NOT NULL,
    tails_location VARCHAR(500),
    tails_hash VARCHAR(255),
    issuer_did VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (cred_def_id) REFERENCES credential_definitions(cred_def_id),
    FOREIGN KEY (issuer_did) REFERENCES dids(did),
    INDEX idx_rev_reg_id (rev_reg_id),
    INDEX idx_cred_def_id (cred_def_id)
);

-- Audit Log table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    actor_did VARCHAR(255),
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    result VARCHAR(50) NOT NULL,  -- success, failure
    metadata JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_event_type (event_type),
    INDEX idx_actor_did (actor_did),
    INDEX idx_created_at (created_at)
);
```

### SQLAlchemy Models
```python
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, JSON, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class DID(Base):
    __tablename__ = 'dids'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    did = Column(String(255), unique=True, nullable=False, index=True)
    verkey = Column(String(255), nullable=False)
    method = Column(String(50), nullable=False, default='indy')
    namespace = Column(String(50), nullable=False, default='sovrin')
    metadata = Column(JSON, default={})
    public = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Credential(Base):
    __tablename__ = 'credentials'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credential_id = Column(String(255), unique=True, nullable=False, index=True)
    credential_exchange_id = Column(String(255))
    holder_did = Column(String(255), ForeignKey('dids.did'), nullable=False, index=True)
    issuer_did = Column(String(255), ForeignKey('dids.did'), nullable=False, index=True)
    schema_id = Column(String(255), ForeignKey('schemas.schema_id'), nullable=False, index=True)
    cred_def_id = Column(String(255), ForeignKey('credential_definitions.cred_def_id'), nullable=False)
    attributes = Column(JSON, nullable=False)
    ipfs_cid = Column(String(255), index=True)
    revocation_reg_id = Column(String(255))
    revocation_index = Column(Integer)
    revoked = Column(Boolean, default=False, index=True)
    revoked_at = Column(TIMESTAMP)
    revocation_reason = Column(String)
    issued_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP)
```

---

## 6. IPFS Metadata

### IPFS File Metadata
```json
{
  "cid": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
  "filename": "diploma.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 245678,
  "uploaded_at": "2025-11-13T19:23:24Z",
  "encrypted": true,
  "encryption_algorithm": "AES-256-GCM",
  "encryption_key_ref": "key_fingerprint_abc123",
  "checksum": {
    "algorithm": "SHA256",
    "value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
}
```

---

**Last Updated**: November 13, 2025
