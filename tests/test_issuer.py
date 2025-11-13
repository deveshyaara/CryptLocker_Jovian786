"""
Test Suite for Issuer Agent
"""

import pytest
import asyncio
from agents.issuer.services.did_service import DIDService
from agents.issuer.services.schema_service import SchemaService
from agents.issuer.services.credential_service import CredentialService
from agents.issuer.services.connection_service import ConnectionService

# Test Configuration
ADMIN_URL = "http://localhost:8030"
API_KEY = "test-api-key"


class TestDIDService:
    """Test DID Service"""
    
    @pytest.fixture
    def did_service(self):
        return DIDService(ADMIN_URL, API_KEY)
    
    @pytest.mark.asyncio
    async def test_create_did(self, did_service):
        """Test DID creation"""
        result = await did_service.create_did()
        assert 'did' in result
        assert 'verkey' in result
        assert result['did'].startswith('did:')
    
    @pytest.mark.asyncio
    async def test_list_dids(self, did_service):
        """Test listing DIDs"""
        result = await did_service.list_dids()
        assert isinstance(result, list)


class TestSchemaService:
    """Test Schema Service"""
    
    @pytest.fixture
    def schema_service(self):
        return SchemaService(ADMIN_URL, API_KEY)
    
    @pytest.mark.asyncio
    async def test_create_schema(self, schema_service):
        """Test schema creation"""
        result = await schema_service.create_schema(
            name="test-schema",
            version="1.0",
            attributes=["name", "degree", "university"]
        )
        assert 'schema_id' in result
    
    @pytest.mark.asyncio
    async def test_create_credential_definition(self, schema_service):
        """Test credential definition creation"""
        # Assumes schema exists
        schema_id = "test-schema-id"
        result = await schema_service.create_credential_definition(
            schema_id=schema_id,
            tag="default"
        )
        assert 'credential_definition_id' in result


class TestCredentialService:
    """Test Credential Service"""
    
    @pytest.fixture
    def credential_service(self):
        return CredentialService(ADMIN_URL, API_KEY)
    
    @pytest.mark.asyncio
    async def test_send_credential_offer(self, credential_service):
        """Test credential offer"""
        result = await credential_service.send_credential_offer(
            connection_id="test-connection-id",
            cred_def_id="test-cred-def-id",
            attributes=[
                {"name": "name", "value": "Alice"},
                {"name": "degree", "value": "BSc"}
            ]
        )
        assert 'credential_exchange_id' in result


class TestConnectionService:
    """Test Connection Service"""
    
    @pytest.fixture
    def connection_service(self):
        return ConnectionService(ADMIN_URL, API_KEY)
    
    @pytest.mark.asyncio
    async def test_create_invitation(self, connection_service):
        """Test invitation creation"""
        result = await connection_service.create_invitation()
        assert 'connection_id' in result
        assert 'invitation_url' in result
    
    @pytest.mark.asyncio
    async def test_list_connections(self, connection_service):
        """Test listing connections"""
        result = await connection_service.list_connections()
        assert isinstance(result, list)


# Integration Tests
class TestIssuerIntegration:
    """Integration tests for complete issuer flow"""
    
    @pytest.mark.asyncio
    async def test_full_issuance_flow(self):
        """Test complete credential issuance flow"""
        did_service = DIDService(ADMIN_URL, API_KEY)
        schema_service = SchemaService(ADMIN_URL, API_KEY)
        cred_service = CredentialService(ADMIN_URL, API_KEY)
        conn_service = ConnectionService(ADMIN_URL, API_KEY)
        
        # Step 1: Create DID
        did_result = await did_service.create_did()
        assert 'did' in did_result
        
        # Step 2: Create Schema
        schema_result = await schema_service.create_schema(
            name="university-degree",
            version="1.0",
            attributes=["name", "degree", "graduation_year"]
        )
        assert 'schema_id' in schema_result
        
        # Step 3: Create Credential Definition
        cred_def_result = await schema_service.create_credential_definition(
            schema_id=schema_result['schema_id']
        )
        assert 'credential_definition_id' in cred_def_result
        
        # Step 4: Create Connection Invitation
        invitation = await conn_service.create_invitation()
        assert 'invitation_url' in invitation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
