"""
Test Suite for Verifier Agent
"""

import pytest
import asyncio
from agents.verifier.services.presentation_service import PresentationService
from agents.verifier.services.connection_service import ConnectionService

# Test Configuration
ADMIN_URL = "http://localhost:8050"
API_KEY = "test-api-key"


class TestPresentationService:
    """Test Presentation Service"""
    
    @pytest.fixture
    def presentation_service(self):
        return PresentationService(ADMIN_URL, API_KEY)
    
    @pytest.mark.asyncio
    async def test_create_proof_request(self, presentation_service):
        """Test proof request creation"""
        result = await presentation_service.create_proof_request(
            name="Test Proof",
            version="1.0",
            requested_attributes={
                "attr1": {
                    "name": "degree",
                    "restrictions": []
                }
            }
        )
        assert 'name' in result
        assert 'requested_attributes' in result
    
    @pytest.mark.asyncio
    async def test_list_presentation_exchanges(self, presentation_service):
        """Test listing presentation exchanges"""
        result = await presentation_service.list_presentation_exchanges()
        assert isinstance(result, list)


class TestVerifierIntegration:
    """Integration tests for complete verifier flow"""
    
    @pytest.mark.asyncio
    async def test_full_verification_flow(self):
        """Test complete proof verification flow"""
        pres_service = PresentationService(ADMIN_URL, API_KEY)
        conn_service = ConnectionService(ADMIN_URL, API_KEY)
        
        # Step 1: Create Connection
        invitation = await conn_service.create_invitation()
        assert 'connection_id' in invitation
        
        # Step 2: Create Proof Request
        proof_request = await pres_service.create_proof_request(
            name="Employment Verification",
            version="1.0",
            requested_attributes={
                "attr1": {
                    "name": "degree",
                    "restrictions": [{"schema_name": "university-degree"}]
                }
            },
            requested_predicates={
                "pred1": {
                    "name": "graduation_year",
                    "p_type": ">=",
                    "p_value": 2020
                }
            }
        )
        assert 'requested_attributes' in proof_request
        assert 'requested_predicates' in proof_request


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
