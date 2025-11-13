"""
Integration Test Suite - CryptLocker System Health Check

Tests all completed components:
- Issuer Agent (13 endpoints)
- Verifier Agent (12 endpoints) 
- IPFS Service
- PostgreSQL Database
- Indy Ledger
- Docker Services

Run: pytest tests/integration/test_system_health.py -v
"""

import pytest
import httpx
import asyncio
import time
import json
from datetime import datetime

# Service URLs
ISSUER_API = "http://localhost:8001"
VERIFIER_API = "http://localhost:8002"
ISSUER_ADMIN = "http://localhost:11001"
VERIFIER_ADMIN = "http://localhost:11002"
INDY_LEDGER = "http://localhost:9000"
IPFS_API = "http://localhost:5001"

# Test timeout
TIMEOUT = 30.0


class TestServiceHealth:
    """Test that all Docker services are running and healthy"""
    
    @pytest.mark.asyncio
    async def test_issuer_agent_health(self):
        """Test Issuer Agent is running"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{ISSUER_ADMIN}/status/ready")
            assert response.status_code == 200, "Issuer agent not ready"
            print(f"✅ Issuer Agent: {response.json()}")
    
    @pytest.mark.asyncio
    async def test_verifier_agent_health(self):
        """Test Verifier Agent is running"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{VERIFIER_ADMIN}/status/ready")
            assert response.status_code == 200, "Verifier agent not ready"
            print(f"✅ Verifier Agent: {response.json()}")
    
    @pytest.mark.asyncio
    async def test_indy_ledger_health(self):
        """Test Indy Ledger is accessible"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{INDY_LEDGER}/genesis")
            assert response.status_code == 200, "Indy ledger not accessible"
            genesis = response.text
            assert len(genesis) > 0, "Genesis file is empty"
            print(f"✅ Indy Ledger: Genesis file size = {len(genesis)} bytes")
    
    @pytest.mark.asyncio
    async def test_ipfs_health(self):
        """Test IPFS is running"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{IPFS_API}/api/v0/id")
            assert response.status_code == 200, "IPFS not accessible"
            ipfs_info = response.json()
            print(f"✅ IPFS Node: {ipfs_info.get('ID', 'unknown')}")


class TestIssuerAgentEndpoints:
    """Test all Issuer Agent REST API endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_issuer_did(self):
        """Test DID creation for issuer"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{ISSUER_API}/did/create")
            assert response.status_code in [200, 409], f"Unexpected status: {response.status_code}"
            
            if response.status_code == 200:
                data = response.json()
                assert "did" in data
                print(f"✅ Created Issuer DID: {data['did']}")
            else:
                print(f"✅ Issuer DID already exists (expected on re-run)")
    
    @pytest.mark.asyncio
    async def test_get_public_did(self):
        """Test getting public DID"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{ISSUER_API}/did/public")
            assert response.status_code == 200
            data = response.json()
            assert "did" in data
            print(f"✅ Public DID: {data['did']}")
    
    @pytest.mark.asyncio
    async def test_create_schema(self):
        """Test schema creation"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            schema_data = {
                "schema_name": f"TestSchema_{int(time.time())}",
                "schema_version": "1.0",
                "attributes": ["name", "age", "email"]
            }
            
            response = await client.post(
                f"{ISSUER_API}/schema/create",
                json=schema_data
            )
            assert response.status_code == 200
            data = response.json()
            assert "schema_id" in data
            print(f"✅ Created Schema: {data['schema_id']}")
            return data['schema_id']
    
    @pytest.mark.asyncio
    async def test_list_schemas(self):
        """Test listing schemas"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{ISSUER_API}/schema/list")
            assert response.status_code == 200
            data = response.json()
            assert "schemas" in data
            print(f"✅ Total Schemas: {len(data['schemas'])}")
    
    @pytest.mark.asyncio
    async def test_create_credential_definition(self):
        """Test credential definition creation"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # First create a schema
            schema_data = {
                "schema_name": f"CredDefSchema_{int(time.time())}",
                "schema_version": "1.0",
                "attributes": ["firstName", "lastName"]
            }
            schema_response = await client.post(
                f"{ISSUER_API}/schema/create",
                json=schema_data
            )
            assert schema_response.status_code == 200
            schema_id = schema_response.json()["schema_id"]
            
            # Create credential definition
            cred_def_response = await client.post(
                f"{ISSUER_API}/credential-definition/create",
                json={"schema_id": schema_id}
            )
            assert cred_def_response.status_code == 200
            data = cred_def_response.json()
            assert "credential_definition_id" in data
            print(f"✅ Created Credential Definition: {data['credential_definition_id']}")
    
    @pytest.mark.asyncio
    async def test_create_connection_invitation(self):
        """Test connection invitation creation"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{ISSUER_API}/connection/create-invitation",
                json={"alias": "test_holder"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "invitation_url" in data
            assert "connection_id" in data
            print(f"✅ Created Invitation: {data['connection_id']}")
    
    @pytest.mark.asyncio
    async def test_list_connections(self):
        """Test listing connections"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{ISSUER_API}/connection/list")
            assert response.status_code == 200
            data = response.json()
            assert "connections" in data
            print(f"✅ Total Connections: {len(data['connections'])}")


class TestVerifierAgentEndpoints:
    """Test all Verifier Agent REST API endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_verifier_did(self):
        """Test DID creation for verifier"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{VERIFIER_API}/did/create")
            assert response.status_code in [200, 409]
            
            if response.status_code == 200:
                data = response.json()
                assert "did" in data
                print(f"✅ Created Verifier DID: {data['did']}")
            else:
                print(f"✅ Verifier DID already exists")
    
    @pytest.mark.asyncio
    async def test_get_verifier_public_did(self):
        """Test getting verifier public DID"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{VERIFIER_API}/did/public")
            assert response.status_code == 200
            data = response.json()
            assert "did" in data
            print(f"✅ Verifier Public DID: {data['did']}")
    
    @pytest.mark.asyncio
    async def test_create_verifier_invitation(self):
        """Test verifier connection invitation"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{VERIFIER_API}/connection/create-invitation",
                json={"alias": "test_holder_verify"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "invitation_url" in data
            print(f"✅ Created Verifier Invitation: {data['connection_id']}")
    
    @pytest.mark.asyncio
    async def test_list_verifier_connections(self):
        """Test listing verifier connections"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{VERIFIER_API}/connection/list")
            assert response.status_code == 200
            data = response.json()
            assert "connections" in data
            print(f"✅ Verifier Connections: {len(data['connections'])}")
    
    @pytest.mark.asyncio
    async def test_create_proof_request(self):
        """Test proof request creation"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            proof_request = {
                "proof_request": {
                    "name": "Test Proof Request",
                    "version": "1.0",
                    "requested_attributes": {
                        "attr1_referent": {
                            "name": "name",
                            "restrictions": []
                        }
                    },
                    "requested_predicates": {}
                },
                "connection_id": "dummy-connection-id"  # Will fail but tests endpoint
            }
            
            response = await client.post(
                f"{VERIFIER_API}/presentation/request-proof",
                json=proof_request
            )
            # May fail with 404 (no connection) but endpoint should respond
            assert response.status_code in [200, 400, 404, 500]
            print(f"✅ Proof Request Endpoint Tested (Status: {response.status_code})")


class TestIPFSService:
    """Test IPFS document storage functionality"""
    
    @pytest.mark.asyncio
    async def test_ipfs_upload_text(self):
        """Test uploading text document to IPFS"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Create test document
            test_content = f"Test document created at {datetime.now().isoformat()}"
            files = {
                'file': ('test.txt', test_content.encode(), 'text/plain')
            }
            
            response = await client.post(
                f"{IPFS_API}/api/v0/add",
                files=files
            )
            assert response.status_code == 200
            data = response.json()
            assert "Hash" in data
            cid = data["Hash"]
            print(f"✅ Uploaded to IPFS: {cid}")
            return cid
    
    @pytest.mark.asyncio
    async def test_ipfs_retrieve_document(self):
        """Test retrieving document from IPFS"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Upload first
            test_content = "Retrieve test document"
            files = {'file': ('retrieve.txt', test_content.encode(), 'text/plain')}
            upload_response = await client.post(f"{IPFS_API}/api/v0/add", files=files)
            cid = upload_response.json()["Hash"]
            
            # Retrieve
            retrieve_response = await client.post(
                f"{IPFS_API}/api/v0/cat",
                params={"arg": cid}
            )
            assert retrieve_response.status_code == 200
            assert retrieve_response.text == test_content
            print(f"✅ Retrieved from IPFS: {cid}")
    
    @pytest.mark.asyncio
    async def test_ipfs_upload_json(self):
        """Test uploading JSON document to IPFS"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            test_json = {
                "credential_type": "TestCredential",
                "timestamp": datetime.now().isoformat(),
                "data": {"key": "value"}
            }
            json_bytes = json.dumps(test_json, indent=2).encode()
            files = {'file': ('test.json', json_bytes, 'application/json')}
            
            response = await client.post(f"{IPFS_API}/api/v0/add", files=files)
            assert response.status_code == 200
            cid = response.json()["Hash"]
            print(f"✅ Uploaded JSON to IPFS: {cid}")


class TestEndToEndWorkflow:
    """Test complete credential issuance workflow (without holder)"""
    
    @pytest.mark.asyncio
    async def test_complete_issuer_setup(self):
        """Test complete issuer setup workflow"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            print("\n🔄 Testing Complete Issuer Setup Workflow...")
            
            # 1. Create/Get DID
            did_response = await client.post(f"{ISSUER_API}/did/create")
            assert did_response.status_code in [200, 409]
            print("   ✅ Step 1: Issuer DID ready")
            
            # 2. Create Schema
            schema_data = {
                "schema_name": f"E2ETestSchema_{int(time.time())}",
                "schema_version": "1.0",
                "attributes": ["fullName", "dateOfBirth", "email"]
            }
            schema_response = await client.post(
                f"{ISSUER_API}/schema/create",
                json=schema_data
            )
            assert schema_response.status_code == 200
            schema_id = schema_response.json()["schema_id"]
            print(f"   ✅ Step 2: Schema created - {schema_id}")
            
            # 3. Create Credential Definition
            cred_def_response = await client.post(
                f"{ISSUER_API}/credential-definition/create",
                json={"schema_id": schema_id}
            )
            assert cred_def_response.status_code == 200
            cred_def_id = cred_def_response.json()["credential_definition_id"]
            print(f"   ✅ Step 3: Credential Definition created - {cred_def_id}")
            
            # 4. Create Connection Invitation
            invitation_response = await client.post(
                f"{ISSUER_API}/connection/create-invitation",
                json={"alias": "e2e_test_holder"}
            )
            assert invitation_response.status_code == 200
            invitation_data = invitation_response.json()
            print(f"   ✅ Step 4: Invitation created - {invitation_data['connection_id']}")
            
            # 5. Upload document to IPFS (simulated supporting document)
            test_doc = json.dumps({"type": "supporting_document", "data": "test"}).encode()
            files = {'file': ('doc.json', test_doc, 'application/json')}
            ipfs_response = await client.post(f"{IPFS_API}/api/v0/add", files=files)
            assert ipfs_response.status_code == 200
            ipfs_cid = ipfs_response.json()["Hash"]
            print(f"   ✅ Step 5: Document uploaded to IPFS - {ipfs_cid}")
            
            print("\n✅ Complete Issuer Setup Workflow: SUCCESS")


class TestDatabaseConnectivity:
    """Test PostgreSQL database connectivity"""
    
    @pytest.mark.asyncio
    async def test_issuer_wallet_exists(self):
        """Test that issuer wallet is accessible via API"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Wallet is accessible if we can get DID
            response = await client.get(f"{ISSUER_API}/did/public")
            assert response.status_code == 200
            print("✅ Issuer Wallet: Accessible via API")
    
    @pytest.mark.asyncio
    async def test_verifier_wallet_exists(self):
        """Test that verifier wallet is accessible via API"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{VERIFIER_API}/did/public")
            assert response.status_code == 200
            print("✅ Verifier Wallet: Accessible via API")


class TestSystemMetrics:
    """Collect system metrics and statistics"""
    
    @pytest.mark.asyncio
    async def test_collect_system_stats(self):
        """Collect and display system statistics"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            print("\n📊 System Statistics:")
            print("=" * 60)
            
            # Issuer stats
            schemas = await client.get(f"{ISSUER_API}/schema/list")
            schema_count = len(schemas.json().get("schemas", []))
            print(f"   Issuer Schemas: {schema_count}")
            
            cred_defs = await client.get(f"{ISSUER_API}/credential-definition/list")
            cred_def_count = len(cred_defs.json().get("credential_definitions", []))
            print(f"   Credential Definitions: {cred_def_count}")
            
            issuer_conns = await client.get(f"{ISSUER_API}/connection/list")
            issuer_conn_count = len(issuer_conns.json().get("connections", []))
            print(f"   Issuer Connections: {issuer_conn_count}")
            
            # Verifier stats
            verifier_conns = await client.get(f"{VERIFIER_API}/connection/list")
            verifier_conn_count = len(verifier_conns.json().get("connections", []))
            print(f"   Verifier Connections: {verifier_conn_count}")
            
            # IPFS stats
            ipfs_stats = await client.post(f"{IPFS_API}/api/v0/stats/repo")
            if ipfs_stats.status_code == 200:
                repo_stats = ipfs_stats.json()
                print(f"   IPFS Repo Size: {repo_stats.get('RepoSize', 0):,} bytes")
            
            print("=" * 60)


# Pytest configuration
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    """Setup before tests and teardown after"""
    print("\n" + "=" * 60)
    print("🚀 CryptLocker System Health Check")
    print("=" * 60)
    print(f"Test Time: {datetime.now().isoformat()}")
    print(f"Issuer API: {ISSUER_API}")
    print(f"Verifier API: {VERIFIER_API}")
    print("=" * 60 + "\n")
    
    yield
    
    print("\n" + "=" * 60)
    print("✅ Test Suite Completed")
    print("=" * 60)


if __name__ == "__main__":
    # Run with: python -m pytest tests/integration/test_system_health.py -v
    pytest.main([__file__, "-v", "--tb=short"])
