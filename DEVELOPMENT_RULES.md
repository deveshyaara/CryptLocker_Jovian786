# 🛠️ Development Rules & Standards

## Purpose
This document establishes coding conventions, architectural principles, and development workflows to ensure consistent, maintainable, and secure code throughout the 24-hour development sprint and beyond.

## 🎯 Core Principles

### 1. Security First
- **All cryptographic operations** must use established libraries (NaCl, libsodium)
- **Never** store private keys in plaintext
- **Always** validate input at API boundaries
- **Use** parameterized queries to prevent injection attacks
- **Implement** rate limiting on all public endpoints

### 2. Privacy by Design
- **Minimize** data collection and storage
- **Implement** selective disclosure by default
- **Use** pairwise DIDs for relationships
- **Avoid** storing unnecessary PII
- **Log** without exposing sensitive data

### 3. Fail Secure
- **Default** to deny access
- **Fail** closed on errors
- **Validate** all inputs explicitly
- **Timeout** long-running operations
- **Revoke** compromised credentials immediately

### 4. Maintainability
- **Write** self-documenting code
- **Comment** complex algorithms and business logic
- **Test** all critical paths
- **Document** API contracts
- **Version** all public interfaces

## 📋 Code Style Guidelines

### Python (Backend - ACA-Py Agents)

#### Style
- Follow **PEP 8** strictly
- Use **Black** formatter (line length: 100)
- Use **isort** for import sorting
- Use **pylint** for linting (minimum score: 8.0)
- Use **mypy** for type checking

#### Naming Conventions
```python
# Classes: PascalCase
class CredentialIssuer:
    pass

# Functions/Methods: snake_case
def create_verifiable_credential(schema_id: str, attributes: dict) -> dict:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_CREDENTIAL_SIZE = 1024 * 1024  # 1MB

# Private methods: _leading_underscore
def _generate_proof_signature(self, data: bytes) -> bytes:
    pass

# Type hints: Always use for function signatures
def verify_presentation(presentation: dict, proof_request: dict) -> bool:
    pass
```

#### Docstrings
```python
def issue_credential(
    issuer_did: str,
    holder_did: str,
    schema_id: str,
    attributes: dict
) -> dict:
    """
    Issue a verifiable credential to a holder.

    Args:
        issuer_did: DID of the credential issuer
        holder_did: DID of the credential holder
        schema_id: Ledger ID of the credential schema
        attributes: Dictionary of credential attributes

    Returns:
        Dictionary containing the issued credential and metadata

    Raises:
        InvalidSchemaError: If schema_id doesn't exist on ledger
        SigningError: If credential signing fails
        
    Example:
        >>> cred = issue_credential(
        ...     "did:indy:sovrin:abc123",
        ...     "did:indy:sovrin:xyz789",
        ...     "schema:degree:1.0",
        ...     {"name": "John Doe", "degree": "BSc"}
        ... )
    """
    pass
```

### JavaScript/TypeScript (Frontend - Wallet UI)

#### Style
- Use **TypeScript** for all new code
- Follow **Airbnb** style guide
- Use **Prettier** formatter
- Use **ESLint** for linting
- **Strict** mode enabled

#### Naming Conventions
```typescript
// Interfaces: PascalCase with 'I' prefix
interface ICredential {
  id: string;
  issuer: string;
  attributes: Record<string, unknown>;
}

// Types: PascalCase
type DIDDocument = {
  id: string;
  publicKey: PublicKey[];
};

// Functions: camelCase
const createPresentation = async (
  credentialIds: string[],
  proofRequest: IProofRequest
): Promise<IPresentation> => {
  // Implementation
};

// React Components: PascalCase
const CredentialCard: React.FC<ICredentialCardProps> = ({ credential }) => {
  return <div>{credential.type}</div>;
};

// Constants: UPPER_SNAKE_CASE
const MAX_RETRY_ATTEMPTS = 3;
```

### SQL (Database Schemas)

```sql
-- Tables: snake_case, plural
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    holder_did VARCHAR(255) NOT NULL,
    credential_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    revoked_at TIMESTAMP NULL,
    
    -- Indexes for common queries
    INDEX idx_holder_did (holder_did),
    INDEX idx_created_at (created_at)
);

-- Always use explicit naming for constraints
ALTER TABLE credentials 
ADD CONSTRAINT fk_credentials_holder 
FOREIGN KEY (holder_did) REFERENCES dids(did);
```

## 🏗️ Architectural Rules

### 1. Separation of Concerns

```
┌─────────────────────────────────────────────┐
│           Presentation Layer                 │  (UI, API Controllers)
├─────────────────────────────────────────────┤
│           Business Logic Layer               │  (Services, Use Cases)
├─────────────────────────────────────────────┤
│           Data Access Layer                  │  (Repositories, DAOs)
├─────────────────────────────────────────────┤
│           Infrastructure Layer               │  (Indy, IPFS, Database)
└─────────────────────────────────────────────┘
```

**Rules**:
- Presentation layer **never** accesses data layer directly
- Business logic **independent** of infrastructure
- Dependencies point **inward** (Dependency Inversion)

### 2. Agent Architecture

Each agent (Issuer, Holder, Verifier) follows this structure:

```
/agents
├── issuer/
│   ├── controllers/     # HTTP API endpoints
│   ├── services/        # Business logic
│   ├── repositories/    # Data access
│   ├── models/          # Domain models
│   ├── utils/           # Helper functions
│   └── config/          # Configuration
├── holder/
└── verifier/
```

### 3. API Design

#### RESTful Conventions
```
POST   /api/v1/dids                    # Create DID
GET    /api/v1/dids/{did}              # Resolve DID
POST   /api/v1/credentials             # Issue credential
GET    /api/v1/credentials/{id}        # Get credential
DELETE /api/v1/credentials/{id}        # Revoke credential
POST   /api/v1/presentations/verify    # Verify presentation
```

#### Response Format
```json
{
  "success": true,
  "data": {
    "credential": {...}
  },
  "meta": {
    "timestamp": "2025-11-13T12:00:00Z",
    "request_id": "req_abc123"
  }
}
```

#### Error Format
```json
{
  "success": false,
  "error": {
    "code": "INVALID_SCHEMA",
    "message": "Schema ID not found on ledger",
    "details": {
      "schema_id": "schema:degree:1.0"
    }
  },
  "meta": {
    "timestamp": "2025-11-13T12:00:00Z",
    "request_id": "req_abc123"
  }
}
```

## 🔒 Security Rules

### 1. Key Management

```python
# ✅ CORRECT: Use secure key derivation
from aries_askar import Key, KeyAlg

key = Key.generate(KeyAlg.ED25519)
# Store encrypted in secure storage

# ❌ WRONG: Never hardcode keys
SECRET_KEY = "abc123..."  # NEVER DO THIS
```

### 2. Input Validation

```python
# ✅ CORRECT: Validate all inputs
def create_credential(schema_id: str, attributes: dict) -> dict:
    if not isinstance(schema_id, str) or not schema_id:
        raise ValueError("Invalid schema_id")
    
    if not isinstance(attributes, dict):
        raise ValueError("Attributes must be a dictionary")
    
    # Validate against schema
    if not validate_schema(schema_id, attributes):
        raise ValidationError("Attributes don't match schema")
    
    return _create_credential_internal(schema_id, attributes)

# ❌ WRONG: Trust user input
def create_credential(schema_id, attributes):
    return _create_credential_internal(schema_id, attributes)
```

### 3. Secrets Management

```python
# ✅ CORRECT: Use environment variables or secret management
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
WALLET_KEY = os.getenv("WALLET_KEY")

# ❌ WRONG: Hardcode in source
DATABASE_URL = "postgresql://user:pass@localhost/db"
```

### 4. Cryptographic Operations

```python
# ✅ CORRECT: Use established libraries
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519

private_key = ed25519.Ed25519PrivateKey.generate()
signature = private_key.sign(data)

# ❌ WRONG: Roll your own crypto
def my_custom_hash(data):
    result = 0
    for byte in data:
        result = (result + byte) % 256
    return result
```

## 🧪 Testing Standards

### Test Coverage Requirements
- **Unit Tests**: Minimum 80% coverage
- **Integration Tests**: All API endpoints
- **E2E Tests**: Critical user workflows

### Test Structure

```python
# tests/unit/test_credential_service.py
import pytest
from services.credential_service import CredentialService

class TestCredentialService:
    """Test suite for CredentialService."""
    
    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return CredentialService()
    
    @pytest.fixture
    def mock_schema(self):
        """Mock credential schema."""
        return {
            "id": "schema:degree:1.0",
            "attributes": ["name", "degree", "university"]
        }
    
    def test_create_credential_success(self, service, mock_schema):
        """Test successful credential creation."""
        # Arrange
        issuer_did = "did:indy:sovrin:abc123"
        holder_did = "did:indy:sovrin:xyz789"
        attributes = {
            "name": "John Doe",
            "degree": "BSc",
            "university": "MIT"
        }
        
        # Act
        credential = service.create_credential(
            issuer_did, holder_did, mock_schema["id"], attributes
        )
        
        # Assert
        assert credential["issuer"] == issuer_did
        assert credential["credentialSubject"]["id"] == holder_did
        assert "proof" in credential
    
    def test_create_credential_invalid_schema(self, service):
        """Test credential creation with invalid schema."""
        with pytest.raises(InvalidSchemaError):
            service.create_credential(
                "did:indy:sovrin:abc123",
                "did:indy:sovrin:xyz789",
                "invalid_schema",
                {}
            )
```

### Test Naming Convention
```
test_<method_name>_<scenario>_<expected_result>

Examples:
- test_verify_presentation_valid_signature_returns_true
- test_revoke_credential_already_revoked_raises_error
- test_create_did_duplicate_raises_conflict
```

## 📦 Dependency Management

### Python
```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"
aries-cloudagent = "^0.11.0"
fastapi = "^0.104.0"
pydantic = "^2.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4"
black = "^23.0"
mypy = "^1.7"
```

**Rules**:
- Pin major and minor versions
- Use `poetry.lock` for reproducible builds
- Review dependencies for security vulnerabilities
- Update dependencies weekly

### JavaScript
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-native": "^0.72.0",
    "@aries-framework/core": "^0.4.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0",
    "jest": "^29.0.0"
  }
}
```

## 🔄 Git Workflow

### Branch Naming
```
feature/<ticket-number>-<short-description>
bugfix/<ticket-number>-<short-description>
hotfix/<ticket-number>-<short-description>
release/<version-number>

Examples:
- feature/SSI-101-implement-did-creation
- bugfix/SSI-205-fix-revocation-check
- hotfix/SSI-301-credential-signature-error
```

### Commit Messages
```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, docs, style, refactor, test, chore

Examples:
feat(issuer): implement credential issuance workflow

- Add CredentialService with create_credential method
- Integrate with Indy ledger for schema validation
- Add unit tests for success and error cases

Closes SSI-101
```

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Error handling doesn't leak sensitive data
- [ ] Crypto operations use approved libraries

## Documentation
- [ ] Code comments added
- [ ] API documentation updated
- [ ] README updated if needed
```

## 📊 Code Review Checklist

### Reviewer Responsibilities
- [ ] Code follows style guidelines
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities introduced
- [ ] Error handling is appropriate
- [ ] Documentation is clear and complete
- [ ] Performance is acceptable
- [ ] Breaking changes are documented

### Review Priorities
1. **Security issues**: Block merge immediately
2. **Correctness**: Verify logic is sound
3. **Testing**: Ensure adequate coverage
4. **Style**: Must follow guidelines
5. **Performance**: Optimize if needed

## 🚀 CI/CD Rules

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    hooks:
      - id: isort
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
```

### CI Pipeline
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          poetry install
          poetry run pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 📝 Documentation Standards

### Code Documentation
- **Every public function**: Docstring required
- **Complex algorithms**: Inline comments explaining logic
- **Magic numbers**: Define as named constants with comments
- **TODOs**: Include ticket number and date

### API Documentation
- Use **OpenAPI 3.0** specification
- Include **examples** for all endpoints
- Document **error codes** and meanings
- Provide **authentication** details

### Architecture Decision Records (ADRs)
```markdown
# ADR-001: Use Hyperledger Indy for DID Registry

## Status
Accepted

## Context
Need a decentralized ledger for storing DIDs and public keys.

## Decision
Use Hyperledger Indy as the DID registry.

## Consequences
- Pros: W3C compliant, proven in production, strong governance
- Cons: Requires running validator nodes, steeper learning curve

## Alternatives Considered
- Ethereum: Higher gas costs, not identity-focused
- ION (Bitcoin): Slower finality, different trust model
```

## 🔐 Security Review Checklist

Before merging any code:
- [ ] No secrets in source code
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] SQL parameterization to prevent injection
- [ ] Rate limiting on public endpoints
- [ ] Authentication and authorization checks
- [ ] Secure random number generation
- [ ] Cryptographic operations use approved libraries
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't expose PII or secrets

## ⚠️ Anti-Patterns to Avoid

### 1. God Objects
```python
# ❌ WRONG: One class does everything
class CredentialManager:
    def create_did(self): pass
    def register_did(self): pass
    def create_schema(self): pass
    def issue_credential(self): pass
    def verify_credential(self): pass
    def revoke_credential(self): pass
    # ... 50 more methods

# ✅ CORRECT: Single Responsibility Principle
class DIDService:
    def create(self): pass
    def register(self): pass

class CredentialService:
    def issue(self): pass
    def verify(self): pass
    def revoke(self): pass
```

### 2. Primitive Obsession
```python
# ❌ WRONG: Using primitives everywhere
def issue_credential(issuer_did: str, holder_did: str) -> dict:
    pass

# ✅ CORRECT: Use domain objects
@dataclass
class DID:
    method: str
    namespace: str
    identifier: str
    
    @property
    def did_string(self) -> str:
        return f"did:{self.method}:{self.namespace}:{self.identifier}"

def issue_credential(issuer_did: DID, holder_did: DID) -> Credential:
    pass
```

### 3. Exception Swallowing
```python
# ❌ WRONG: Silent failures
try:
    result = risky_operation()
except Exception:
    pass  # Errors disappear

# ✅ CORRECT: Handle or propagate
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise ServiceError("Could not complete operation") from e
```

## 📚 Required Reading

Before contributing, developers must review:
1. [Hyperledger Aries RFC 0036](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0036-issue-credential) - Issue Credential Protocol
2. [W3C DID Core Specification](https://www.w3.org/TR/did-core/)
3. [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
4. [DIDComm Messaging Specification](https://identity.foundation/didcomm-messaging/spec/)

## 🎓 Onboarding Checklist

New developers must complete:
- [ ] Read this document thoroughly
- [ ] Set up development environment
- [ ] Run all tests successfully
- [ ] Complete security training
- [ ] Review architecture documentation
- [ ] Submit first PR (documentation improvement)

---

**Enforcement**: All PRs will be reviewed against these standards. Non-compliant code will not be merged.

**Updates**: This document is versioned. Last updated: November 13, 2025.
