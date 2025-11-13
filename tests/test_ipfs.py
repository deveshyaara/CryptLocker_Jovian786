"""
Test Suite for IPFS Service
"""

import pytest
import asyncio
from shared.services.ipfs_service import IPFSService

# Test Configuration
IPFS_API_URL = "http://localhost:5001"
IPFS_GATEWAY_URL = "http://localhost:8080"


class TestIPFSService:
    """Test IPFS Service"""
    
    @pytest.fixture
    def ipfs_service(self):
        return IPFSService(IPFS_API_URL, IPFS_GATEWAY_URL)
    
    @pytest.mark.asyncio
    async def test_node_reachable(self, ipfs_service):
        """Test IPFS node connectivity"""
        result = await ipfs_service.is_reachable()
        assert result is True
    
    @pytest.mark.asyncio
    async def test_get_node_id(self, ipfs_service):
        """Test getting IPFS node ID"""
        node_id = await ipfs_service.get_node_id()
        assert node_id is not None
        assert len(node_id) > 0
    
    @pytest.mark.asyncio
    async def test_add_json(self, ipfs_service):
        """Test uploading JSON to IPFS"""
        test_data = {
            "name": "Test Document",
            "type": "credential",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        result = await ipfs_service.add_json(test_data)
        assert 'cid' in result
        assert 'hash' in result
    
    @pytest.mark.asyncio
    async def test_add_and_retrieve_file(self, ipfs_service):
        """Test uploading and retrieving file"""
        test_content = b"Hello, IPFS!"
        
        # Upload
        upload_result = await ipfs_service.add_file(
            file_data=test_content,
            filename="test.txt",
            mime_type="text/plain"
        )
        cid = upload_result['cid']
        
        # Retrieve
        retrieved_content = await ipfs_service.get_file(cid)
        assert retrieved_content == test_content
    
    @pytest.mark.asyncio
    async def test_pin_operations(self, ipfs_service):
        """Test pinning content"""
        test_content = b"Pinned content"
        
        # Upload
        result = await ipfs_service.add_file(test_content, "pinned.txt")
        cid = result['cid']
        
        # Pin
        pin_result = await ipfs_service.pin_add(cid)
        assert 'Pins' in pin_result
    
    @pytest.mark.asyncio
    async def test_integrity_verification(self, ipfs_service):
        """Test file integrity verification"""
        test_content = b"Integrity test content"
        
        # Upload
        result = await ipfs_service.add_file(test_content, "integrity.txt")
        cid = result['cid']
        expected_hash = result['hash']
        
        # Verify
        is_valid = await ipfs_service.verify_integrity(cid, expected_hash)
        assert is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
