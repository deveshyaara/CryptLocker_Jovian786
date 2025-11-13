"""
IPFS Service for Document Storage
Handles document upload, retrieval, and metadata management
"""

import logging
import aiohttp
import asyncio
from typing import Dict, Optional, List, BinaryIO
import hashlib
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class IPFSService:
    """Service for interacting with IPFS"""
    
    def __init__(self, api_url: str, gateway_url: str):
        """
        Initialize IPFS Service
        
        Args:
            api_url: IPFS API URL (e.g., http://localhost:5001)
            gateway_url: IPFS Gateway URL (e.g., http://localhost:8080)
        """
        self.api_url = api_url.rstrip('/')
        self.gateway_url = gateway_url.rstrip('/')
    
    async def add_file(
        self,
        file_data: bytes,
        filename: str,
        mime_type: Optional[str] = None
    ) -> Dict:
        """
        Upload file to IPFS
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            mime_type: MIME type of the file
            
        Returns:
            Dict with CID and metadata
            
        Example:
            {
                "cid": "QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco",
                "size": 12345,
                "filename": "degree.pdf",
                "mime_type": "application/pdf",
                "hash": "sha256:...",
                "uploaded_at": "2024-01-01T00:00:00Z"
            }
        """
        endpoint = f"{self.api_url}/api/v0/add"
        
        # Calculate hash for integrity verification
        file_hash = hashlib.sha256(file_data).hexdigest()
        
        # Prepare form data
        form_data = aiohttp.FormData()
        form_data.add_field(
            'file',
            file_data,
            filename=filename,
            content_type=mime_type or 'application/octet-stream'
        )
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, data=form_data) as response:
                response.raise_for_status()
                result = await response.json()
                
                cid = result['Hash']
                logger.info(f"Uploaded file to IPFS: {cid}")
                
                return {
                    "cid": cid,
                    "size": result['Size'],
                    "filename": filename,
                    "mime_type": mime_type,
                    "hash": f"sha256:{file_hash}",
                    "uploaded_at": datetime.utcnow().isoformat() + "Z"
                }
    
    async def add_json(self, data: Dict, name: str = "data.json") -> Dict:
        """
        Upload JSON data to IPFS
        
        Args:
            data: Dictionary to upload
            name: Name for the JSON file
            
        Returns:
            Dict with CID and metadata
        """
        json_bytes = json.dumps(data, indent=2).encode('utf-8')
        return await self.add_file(json_bytes, name, "application/json")
    
    async def get_file(self, cid: str) -> bytes:
        """
        Retrieve file from IPFS by CID
        
        Args:
            cid: Content Identifier
            
        Returns:
            File content as bytes
        """
        endpoint = f"{self.gateway_url}/ipfs/{cid}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                response.raise_for_status()
                content = await response.read()
                logger.info(f"Retrieved file from IPFS: {cid}")
                return content
    
    async def get_json(self, cid: str) -> Dict:
        """
        Retrieve JSON data from IPFS
        
        Args:
            cid: Content Identifier
            
        Returns:
            Parsed JSON as dictionary
        """
        content = await self.get_file(cid)
        return json.loads(content.decode('utf-8'))
    
    async def pin_add(self, cid: str) -> Dict:
        """
        Pin content to ensure it's not garbage collected
        
        Args:
            cid: Content Identifier to pin
            
        Returns:
            Pin status
        """
        endpoint = f"{self.api_url}/api/v0/pin/add"
        params = {"arg": cid}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, params=params) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Pinned content: {cid}")
                return result
    
    async def pin_remove(self, cid: str) -> Dict:
        """
        Unpin content (allow garbage collection)
        
        Args:
            cid: Content Identifier to unpin
            
        Returns:
            Unpin status
        """
        endpoint = f"{self.api_url}/api/v0/pin/rm"
        params = {"arg": cid}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, params=params) as response:
                response.raise_for_status()
                result = await response.json()
                logger.warning(f"Unpinned content: {cid}")
                return result
    
    async def get_stats(self, cid: str) -> Dict:
        """
        Get statistics about content
        
        Args:
            cid: Content Identifier
            
        Returns:
            Stats including size, blocks, etc.
        """
        endpoint = f"{self.api_url}/api/v0/object/stat"
        params = {"arg": cid}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, params=params) as response:
                response.raise_for_status()
                return await response.json()
    
    async def verify_integrity(self, cid: str, expected_hash: str) -> bool:
        """
        Verify file integrity by comparing hash
        
        Args:
            cid: Content Identifier
            expected_hash: Expected SHA-256 hash (format: "sha256:...")
            
        Returns:
            True if hash matches, False otherwise
        """
        try:
            content = await self.get_file(cid)
            actual_hash = "sha256:" + hashlib.sha256(content).hexdigest()
            
            matches = actual_hash == expected_hash
            if matches:
                logger.info(f"Integrity verified for {cid}")
            else:
                logger.error(f"Integrity check failed for {cid}")
            
            return matches
        except Exception as e:
            logger.error(f"Error verifying integrity: {e}")
            return False
    
    async def is_reachable(self) -> bool:
        """
        Check if IPFS node is reachable
        
        Returns:
            True if node is reachable, False otherwise
        """
        try:
            endpoint = f"{self.api_url}/api/v0/version"
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"IPFS node unreachable: {e}")
            return False
    
    async def get_node_id(self) -> Optional[str]:
        """
        Get IPFS node ID
        
        Returns:
            Node ID or None if error
        """
        try:
            endpoint = f"{self.api_url}/api/v0/id"
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result.get('ID')
        except Exception as e:
            logger.error(f"Failed to get node ID: {e}")
            return None
    
    def get_gateway_url(self, cid: str) -> str:
        """
        Get full gateway URL for a CID
        
        Args:
            cid: Content Identifier
            
        Returns:
            Full URL to access content via gateway
        """
        return f"{self.gateway_url}/ipfs/{cid}"
    
    async def add_directory(self, files: List[Dict]) -> Dict:
        """
        Upload multiple files as a directory
        
        Args:
            files: List of dicts with 'name', 'data', 'mime_type'
            
        Returns:
            Dict with directory CID and file CIDs
        """
        endpoint = f"{self.api_url}/api/v0/add"
        
        form_data = aiohttp.FormData()
        for file_info in files:
            form_data.add_field(
                'file',
                file_info['data'],
                filename=file_info['name'],
                content_type=file_info.get('mime_type', 'application/octet-stream')
            )
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                data=form_data,
                params={"wrap-with-directory": "true"}
            ) as response:
                response.raise_for_status()
                
                # Parse response (multiple JSON objects)
                text = await response.text()
                results = [json.loads(line) for line in text.strip().split('\n')]
                
                # Last result is the directory
                directory_cid = results[-1]['Hash']
                file_cids = {r['Name']: r['Hash'] for r in results[:-1]}
                
                logger.info(f"Uploaded directory to IPFS: {directory_cid}")
                
                return {
                    "directory_cid": directory_cid,
                    "files": file_cids
                }
