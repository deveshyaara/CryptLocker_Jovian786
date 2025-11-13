# Security & Governance Framework

## Table of Contents
1. [Security Architecture](#security-architecture)
2. [Key Management](#key-management)
3. [Cryptographic Standards](#cryptographic-standards)
4. [Access Control](#access-control)
5. [Network Security](#network-security)
6. [Privacy Protection](#privacy-protection)
7. [Governance Model](#governance-model)
8. [Incident Response](#incident-response)

---

## 1. Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────────┐
│ Layer 7: Governance & Compliance                        │
├─────────────────────────────────────────────────────────┤
│ Layer 6: Application Security (Input Validation)        │
├─────────────────────────────────────────────────────────┤
│ Layer 5: Wallet Security (Encrypted Storage)            │
├─────────────────────────────────────────────────────────┤
│ Layer 4: Key Management (HSM, Secure Enclave)           │
├─────────────────────────────────────────────────────────┤
│ Layer 3: Network Security (TLS, DIDComm Encryption)     │
├─────────────────────────────────────────────────────────┤
│ Layer 2: Infrastructure Security (Docker, Firewall)     │
├─────────────────────────────────────────────────────────┤
│ Layer 1: Physical Security (Ledger Nodes)               │
└─────────────────────────────────────────────────────────┘
```

### Security Principles

1. **Zero Trust**: Never trust, always verify
2. **Least Privilege**: Minimum necessary permissions
3. **Defense in Depth**: Multiple security layers
4. **Privacy by Design**: Privacy-first architecture
5. **Fail Secure**: Default to deny on errors

---

## 2. Key Management

### Key Types and Usage

| Key Type | Algorithm | Purpose | Storage | Rotation |
|----------|-----------|---------|---------|----------|
| **DID Signing Key** | Ed25519 | Sign VCs, authenticate | HSM/Secure Enclave | Never (tied to DID) |
| **DIDComm Encryption Key** | X25519 | Encrypt messages | HSM/Secure Enclave | Annually |
| **Wallet Encryption Key** | ChaCha20-Poly1305 | Encrypt wallet data | Derived from passphrase | On passphrase change |
| **API Keys** | Random 256-bit | Authenticate API requests | Environment variables | Quarterly |
| **Database Encryption Key** | AES-256-GCM | Encrypt sensitive fields | Key management service | Annually |

### Key Generation

```python
from aries_askar import Key, KeyAlg
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import secrets
import os

class KeyManager:
    """Secure key generation and management."""
    
    @staticmethod
    def generate_did_keys() -> tuple[str, str]:
        """Generate Ed25519 key pair for DID.
        
        Returns:
            tuple: (private_key, public_key) in hex format
        """
        key = Key.generate(KeyAlg.ED25519)
        private_key = key.get_secret_bytes().hex()
        public_key = key.get_public_bytes().hex()
        return private_key, public_key
    
    @staticmethod
    def derive_wallet_key(passphrase: str, salt: bytes = None) -> bytes:
        """Derive wallet encryption key from passphrase using PBKDF2.
        
        Args:
            passphrase: User's wallet passphrase
            salt: Optional salt (generated if not provided)
            
        Returns:
            bytes: 32-byte encryption key
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000,  # OWASP recommendation
        )
        key = kdf.derive(passphrase.encode('utf-8'))
        return key, salt
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate secure API key.
        
        Returns:
            str: 64-character hex API key
        """
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_mnemonic() -> str:
        """Generate BIP39 mnemonic for wallet recovery.
        
        Returns:
            str: 24-word mnemonic phrase
        """
        from aries_askar import generate_raw_key
        # Generate 256-bit entropy
        entropy = secrets.token_bytes(32)
        # Convert to BIP39 mnemonic (implementation depends on library)
        # This is a placeholder - use proper BIP39 library
        return "word1 word2 ... word24"
```

### Key Storage

#### Development Environment
```python
# Store in encrypted file
from cryptography.fernet import Fernet

class KeyStorage:
    def __init__(self, master_key: bytes):
        self.cipher = Fernet(master_key)
    
    def store_key(self, key_id: str, key_data: bytes) -> None:
        """Encrypt and store key."""
        encrypted = self.cipher.encrypt(key_data)
        with open(f"keys/{key_id}.enc", "wb") as f:
            f.write(encrypted)
    
    def retrieve_key(self, key_id: str) -> bytes:
        """Retrieve and decrypt key."""
        with open(f"keys/{key_id}.enc", "rb") as f:
            encrypted = f.read()
        return self.cipher.decrypt(encrypted)
```

#### Production Environment
```python
# Use Hardware Security Module (HSM) or Cloud KMS
import boto3

class ProductionKeyStorage:
    def __init__(self):
        self.kms_client = boto3.client('kms')
    
    def store_key(self, key_id: str, key_data: bytes) -> None:
        """Store key in AWS KMS."""
        self.kms_client.create_key(
            Description=f"SSI Key: {key_id}",
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS'
        )
    
    def encrypt_with_kms(self, plaintext: bytes, key_id: str) -> bytes:
        """Encrypt data using KMS key."""
        response = self.kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext
        )
        return response['CiphertextBlob']
```

### Key Rotation Policy

```yaml
key_rotation:
  did_signing_keys:
    rotate: never
    reason: "Tied to DID identity - rotation requires DID update"
    
  didcomm_encryption_keys:
    rotate: annually
    process:
      - Generate new X25519 key pair
      - Update DID Document with new keyAgreement
      - Publish update to ledger
      - Notify connections via key-rotation protocol
      - Deprecate old key after 30-day grace period
    
  wallet_encryption_keys:
    rotate: on_passphrase_change
    process:
      - Derive new key from new passphrase
      - Re-encrypt all wallet data
      - Securely delete old key
    
  api_keys:
    rotate: quarterly
    process:
      - Generate new API key
      - Distribute to authorized services
      - Deprecate old key after 7-day grace period
      - Revoke old key
```

---

## 3. Cryptographic Standards

### Approved Algorithms

#### Signing
- **Ed25519**: DID signatures, credential signatures
- **ECDSA (secp256k1)**: Bitcoin/Ethereum compatibility

#### Encryption
- **ChaCha20-Poly1305**: Wallet encryption, message encryption
- **AES-256-GCM**: Database encryption, file encryption
- **X25519**: Key agreement for DIDComm

#### Hashing
- **SHA-256**: Content addressing, credential hashes
- **SHA-512**: BIP39 mnemonic derivation
- **BLAKE2b**: High-speed hashing

#### Key Derivation
- **PBKDF2** (600k+ iterations): Passphrase-based key derivation
- **Argon2id**: Memory-hard KDF (preferred for new systems)

### Cryptographic Implementation

```python
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
import hashlib

class CryptoService:
    """Centralized cryptographic operations."""
    
    @staticmethod
    def sign_data(private_key_bytes: bytes, data: bytes) -> bytes:
        """Sign data with Ed25519 private key."""
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
            private_key_bytes
        )
        signature = private_key.sign(data)
        return signature
    
    @staticmethod
    def verify_signature(
        public_key_bytes: bytes,
        signature: bytes,
        data: bytes
    ) -> bool:
        """Verify Ed25519 signature."""
        try:
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(
                public_key_bytes
            )
            public_key.verify(signature, data)
            return True
        except Exception:
            return False
    
    @staticmethod
    def encrypt_data(key: bytes, plaintext: bytes, aad: bytes = b'') -> bytes:
        """Encrypt data with ChaCha20-Poly1305."""
        cipher = ChaCha20Poly1305(key)
        nonce = secrets.token_bytes(12)  # 96-bit nonce
        ciphertext = cipher.encrypt(nonce, plaintext, aad)
        return nonce + ciphertext  # Prepend nonce
    
    @staticmethod
    def decrypt_data(key: bytes, ciphertext_with_nonce: bytes, aad: bytes = b'') -> bytes:
        """Decrypt data with ChaCha20-Poly1305."""
        cipher = ChaCha20Poly1305(key)
        nonce = ciphertext_with_nonce[:12]
        ciphertext = ciphertext_with_nonce[12:]
        plaintext = cipher.decrypt(nonce, ciphertext, aad)
        return plaintext
    
    @staticmethod
    def hash_data(data: bytes, algorithm: str = 'sha256') -> str:
        """Hash data with specified algorithm."""
        if algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        elif algorithm == 'blake2b':
            return hashlib.blake2b(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
```

---

## 4. Access Control

### Role-Based Access Control (RBAC)

```yaml
roles:
  admin:
    permissions:
      - create_schema
      - create_cred_def
      - revoke_credential
      - manage_users
      - view_audit_logs
    
  issuer:
    permissions:
      - issue_credential
      - revoke_credential
      - view_issued_credentials
      - create_connection
    
  verifier:
    permissions:
      - request_proof
      - verify_presentation
      - view_verification_history
      - create_connection
    
  holder:
    permissions:
      - accept_credential
      - create_presentation
      - manage_connections
      - export_backup
```

### API Authentication

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header)
) -> str:
    """Verify API key and return associated DID."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    
    # Check API key in database
    did = await get_did_for_api_key(api_key)
    if not did:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    # Check rate limit
    if not await check_rate_limit(did):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    return did

# Usage in FastAPI endpoint
@app.post("/credentials/issue")
async def issue_credential(
    request: CredentialRequest,
    issuer_did: str = Depends(verify_api_key)
):
    # issuer_did is authenticated
    pass
```

### Rate Limiting

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self):
        self.buckets = defaultdict(lambda: {
            'tokens': 100,
            'last_update': datetime.now()
        })
    
    def check_limit(
        self,
        identifier: str,
        max_tokens: int = 100,
        refill_rate: int = 10  # tokens per minute
    ) -> bool:
        """Check if request is within rate limit."""
        bucket = self.buckets[identifier]
        now = datetime.now()
        
        # Refill tokens based on time passed
        time_passed = (now - bucket['last_update']).total_seconds() / 60
        tokens_to_add = int(time_passed * refill_rate)
        bucket['tokens'] = min(max_tokens, bucket['tokens'] + tokens_to_add)
        bucket['last_update'] = now
        
        # Check if request can be served
        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            return True
        else:
            return False
```

---

## 5. Network Security

### TLS Configuration

```yaml
# nginx.conf
server {
    listen 443 ssl http2;
    server_name agent.example.com;
    
    ssl_certificate /etc/ssl/certs/agent.crt;
    ssl_certificate_key /etc/ssl/private/agent.key;
    
    # TLS 1.3 only
    ssl_protocols TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384';
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Other security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://localhost:8020;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### DIDComm Message Security

```python
from didcomm_messaging import Message, PackedMessage

class DIDCommSecurity:
    """Secure DIDComm message handling."""
    
    async def pack_message(
        self,
        message: dict,
        to_did: str,
        from_did: str
    ) -> bytes:
        """Pack message with authenticated encryption."""
        # Get recipient's public key from DID Document
        recipient_key = await self.resolve_encryption_key(to_did)
        
        # Get sender's private key
        sender_key = await self.get_private_key(from_did)
        
        # Pack message (authenticated encryption)
        packed = await Message.pack(
            message=message,
            to_keys=[recipient_key],
            from_key=sender_key,
            sign_by=sender_key  # Sign for authenticity
        )
        
        return packed
    
    async def unpack_message(
        self,
        packed_message: bytes,
        my_did: str
    ) -> dict:
        """Unpack and verify DIDComm message."""
        # Get private key
        my_key = await self.get_private_key(my_did)
        
        # Unpack message
        unpacked = await Message.unpack(
            packed_message=packed_message,
            to_key=my_key
        )
        
        # Verify sender
        if not unpacked.sender_verified:
            raise SecurityError("Sender could not be verified")
        
        # Verify message integrity
        if not unpacked.authenticated:
            raise SecurityError("Message authentication failed")
        
        return unpacked.message
```

---

## 6. Privacy Protection

### Zero-Knowledge Proofs (ZKPs)

```python
from anoncreds import Credential, CredentialRequest, Proof

class PrivacyService:
    """Privacy-preserving credential operations."""
    
    async def create_selective_disclosure(
        self,
        credential: dict,
        proof_request: dict,
        revealed_attributes: list[str]
    ) -> dict:
        """Create ZKP revealing only specified attributes."""
        
        # Build proof with selective disclosure
        proof = await Proof.create(
            proof_request=proof_request,
            credentials={
                credential['referent']: {
                    'credential': credential,
                    'revealed_attributes': revealed_attributes,
                    'unrevealed_attributes': [
                        attr for attr in credential['attributes']
                        if attr not in revealed_attributes
                    ]
                }
            }
        )
        
        return proof
    
    async def prove_predicate(
        self,
        credential: dict,
        attribute_name: str,
        predicate_type: str,  # '>=', '>', '<=', '<'
        predicate_value: int
    ) -> dict:
        """Prove predicate without revealing actual value."""
        
        proof_request = {
            'requested_predicates': {
                'predicate1': {
                    'name': attribute_name,
                    'p_type': predicate_type,
                    'p_value': predicate_value
                }
            }
        }
        
        proof = await Proof.create(
            proof_request=proof_request,
            credentials={credential['referent']: credential}
        )
        
        # Proof contains YES/NO for predicate, NOT actual value
        return proof
```

### Pairwise DIDs

```python
class PairwiseDIDManager:
    """Manage pairwise DIDs for unlinkability."""
    
    async def create_pairwise_did(
        self,
        my_public_did: str,
        their_did: str
    ) -> str:
        """Create unique pairwise DID for relationship."""
        
        # Generate new key pair
        private_key, public_key = KeyManager.generate_did_keys()
        
        # Create pairwise DID (not published to ledger)
        pairwise_did = f"did:peer:{public_key[:16]}"
        
        # Store relationship
        await self.store_pairwise_relationship(
            my_public_did=my_public_did,
            pairwise_did=pairwise_did,
            their_did=their_did,
            private_key=private_key
        )
        
        return pairwise_did
```

### Data Minimization

```python
class DataMinimization:
    """Ensure minimal data collection and retention."""
    
    @staticmethod
    def filter_attributes(
        all_attributes: dict,
        required_attributes: list[str]
    ) -> dict:
        """Return only required attributes."""
        return {
            key: value
            for key, value in all_attributes.items()
            if key in required_attributes
        }
    
    @staticmethod
    async def auto_delete_old_data():
        """Delete data past retention period."""
        retention_days = 90
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Delete old presentations
        await db.execute(
            "DELETE FROM presentations WHERE created_at < :cutoff",
            {"cutoff": cutoff_date}
        )
        
        # Delete old audit logs (keep for compliance)
        await db.execute(
            "DELETE FROM audit_logs WHERE created_at < :cutoff AND event_type NOT IN ('credential_issued', 'credential_revoked')",
            {"cutoff": cutoff_date}
        )
```

---

## 7. Governance Model

### Consortium Governance

```yaml
governance_structure:
  stewards:
    - name: "Government Ledger Authority"
      role: "Ledger operation, validator node"
      voting_power: 1
    
    - name: "University Consortium"
      role: "Schema governance, credential standards"
      voting_power: 1
    
    - name: "Financial Services Alliance"
      role: "Compliance, security standards"
      voting_power: 1
    
    - name: "Healthcare Network"
      role: "Privacy standards, audit"
      voting_power: 1
  
  decision_making:
    schema_approval:
      threshold: "51% of stewards"
      process:
        - Schema proposal submitted
        - 7-day review period
        - Vote by stewards
        - If approved, publish to ledger
    
    cred_def_approval:
      threshold: "Any 2 stewards approve issuer"
      process:
        - Issuer KYC verification
        - Background check
        - Steward approval
        - Issue credential definition
    
    revocation_dispute:
      threshold: "75% of stewards"
      process:
        - Dispute filed
        - Evidence review
        - Hearing (if needed)
        - Vote on resolution
        - Binding decision
```

### Schema Governance

```python
from enum import Enum
from datetime import datetime

class SchemaStatus(Enum):
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"

class SchemaGovernance:
    """Manage schema lifecycle and approvals."""
    
    async def propose_schema(
        self,
        name: str,
        version: str,
        attributes: list[str],
        proposer_did: str,
        rationale: str
    ) -> str:
        """Submit schema proposal for review."""
        
        schema_proposal = {
            'id': f"proposal:{secrets.token_hex(8)}",
            'name': name,
            'version': version,
            'attributes': attributes,
            'proposer_did': proposer_did,
            'rationale': rationale,
            'status': SchemaStatus.PROPOSED,
            'submitted_at': datetime.now(),
            'votes': {},
            'comments': []
        }
        
        # Store proposal
        await self.db.store_schema_proposal(schema_proposal)
        
        # Notify stewards
        await self.notify_stewards(schema_proposal)
        
        return schema_proposal['id']
    
    async def vote_on_schema(
        self,
        proposal_id: str,
        steward_did: str,
        vote: bool,  # True = approve, False = reject
        comment: str = ""
    ):
        """Steward votes on schema proposal."""
        
        # Verify steward authority
        if not await self.is_steward(steward_did):
            raise PermissionError("Not a steward")
        
        # Record vote
        proposal = await self.db.get_schema_proposal(proposal_id)
        proposal['votes'][steward_did] = {
            'vote': vote,
            'comment': comment,
            'timestamp': datetime.now()
        }
        
        # Check if threshold met
        if self.check_approval_threshold(proposal):
            await self.approve_schema(proposal)
        elif self.check_rejection_threshold(proposal):
            await self.reject_schema(proposal)
```

---

## 8. Incident Response

### Security Incident Classification

| Severity | Description | Response Time | Examples |
|----------|-------------|---------------|----------|
| **P0 - Critical** | Active exploit, data breach | Immediate | Private key compromise, ledger attack |
| **P1 - High** | Vulnerability found, no active exploit | 24 hours | Unpatched CVE, config error |
| **P2 - Medium** | Potential vulnerability | 7 days | Deprecated algorithm use |
| **P3 - Low** | Best practice violation | 30 days | Missing security header |

### Incident Response Plan

```yaml
incident_response:
  detection:
    - Automated monitoring alerts
    - Security audit findings
    - User reports
    - Penetration test results
  
  response_phases:
    1_identification:
      actions:
        - Confirm incident
        - Classify severity
        - Assemble response team
        - Begin logging all actions
      
    2_containment:
      actions:
        - Isolate affected systems
        - Rotate compromised keys
        - Revoke compromised credentials
        - Block malicious actors
      
    3_eradication:
      actions:
        - Remove malware/exploit
        - Patch vulnerabilities
        - Update security controls
        - Verify system integrity
      
    4_recovery:
      actions:
        - Restore services
        - Verify security
        - Monitor for recurrence
        - Notify affected users
      
    5_lessons_learned:
      actions:
        - Incident report
        - Root cause analysis
        - Update procedures
        - Training for team
```

### Key Compromise Response

```python
class IncidentResponse:
    """Handle security incidents."""
    
    async def handle_key_compromise(
        self,
        compromised_did: str,
        key_type: str
    ):
        """Respond to key compromise incident."""
        
        # 1. Immediately rotate key
        new_private_key, new_public_key = KeyManager.generate_did_keys()
        
        # 2. Update DID Document on ledger
        await self.update_did_document(
            did=compromised_did,
            new_public_key=new_public_key,
            reason="Key compromise"
        )
        
        # 3. Revoke all credentials issued with compromised key
        credentials = await self.get_credentials_by_issuer(compromised_did)
        for cred in credentials:
            await self.revoke_credential(
                cred.id,
                reason="Issuer key compromise"
            )
        
        # 4. Notify all verifiers
        await self.notify_verifiers(
            message="Credential issuer key compromised. Re-verify all presentations.",
            issuer_did=compromised_did
        )
        
        # 5. Log incident
        await self.log_security_incident(
            incident_type="KEY_COMPROMISE",
            affected_did=compromised_did,
            actions_taken=[
                "Key rotated",
                f"{len(credentials)} credentials revoked",
                "Verifiers notified"
            ]
        )
```

---

## Security Audit Checklist

### Pre-Production Security Review

- [ ] All cryptographic operations use approved algorithms
- [ ] Private keys never stored in plaintext
- [ ] All API endpoints have authentication
- [ ] Rate limiting implemented
- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection enabled
- [ ] TLS 1.3 enforced
- [ ] Security headers configured
- [ ] Secrets not in source code
- [ ] Dependency vulnerability scan passed
- [ ] Penetration test completed
- [ ] Incident response plan documented
- [ ] Backup and recovery tested
- [ ] Access control properly configured
- [ ] Audit logging enabled
- [ ] Data retention policy enforced
- [ ] Privacy impact assessment completed
- [ ] Compliance requirements met

---

**Last Updated**: November 13, 2025  
**Version**: 1.0  
**Classification**: Internal Use
