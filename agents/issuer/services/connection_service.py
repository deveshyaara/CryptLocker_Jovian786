"""
Connection Service for Issuer Agent
Manages DIDComm connections with holders and verifiers
"""

import logging
from typing import Dict, List, Optional
import aiohttp

logger = logging.getLogger(__name__)


class ConnectionService:
    """Service for managing peer-to-peer connections"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Connection Service
        
        Args:
            admin_url: ACA-Py admin API URL
            api_key: Admin API key for authentication
        """
        self.admin_url = admin_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    async def create_invitation(
        self,
        alias: Optional[str] = None,
        multi_use: bool = False,
        public: bool = False
    ) -> Dict:
        """
        Create a connection invitation
        
        Args:
            alias: Optional alias for the connection
            multi_use: Allow multiple connections from this invitation
            public: Use public DID instead of peer DID
            
        Returns:
            Invitation details including invitation URL
            
        Example:
            {
                "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "invitation": {...},
                "invitation_url": "http://example.com?c_i=eyJAdHlwZSI6Li4u"
            }
        """
        endpoint = f"{self.admin_url}/connections/create-invitation"
        params = {}
        
        if alias:
            params["alias"] = alias
        if multi_use:
            params["multi_use"] = "true"
        if public:
            params["public"] = "true"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Created invitation: {result.get('connection_id')}")
                return result
    
    async def receive_invitation(self, invitation: Dict, alias: Optional[str] = None) -> Dict:
        """
        Receive and accept a connection invitation
        
        Args:
            invitation: Invitation object
            alias: Optional alias for the connection
            
        Returns:
            Connection record
        """
        endpoint = f"{self.admin_url}/connections/receive-invitation"
        params = {}
        
        if alias:
            params["alias"] = alias
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                params=params,
                json=invitation
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Received invitation: {result.get('connection_id')}")
                return result
    
    async def accept_invitation(self, connection_id: str) -> Dict:
        """
        Accept a connection invitation
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Updated connection record
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}/accept-invitation"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Accepted invitation: {connection_id}")
                return result
    
    async def accept_request(self, connection_id: str) -> Dict:
        """
        Accept a connection request
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Updated connection record
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}/accept-request"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Accepted request: {connection_id}")
                return result
    
    async def get_connection(self, connection_id: str) -> Dict:
        """
        Get connection details
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Connection record
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def list_connections(
        self,
        alias: Optional[str] = None,
        state: Optional[str] = None,
        their_role: Optional[str] = None
    ) -> List[Dict]:
        """
        List connections
        
        Args:
            alias: Filter by alias
            state: Filter by state (e.g., "active", "invitation", "request")
            their_role: Filter by their role (e.g., "inviter", "invitee")
            
        Returns:
            List of connection records
        """
        endpoint = f"{self.admin_url}/connections"
        params = {}
        
        if alias:
            params["alias"] = alias
        if state:
            params["state"] = state
        if their_role:
            params["their_role"] = their_role
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('results', [])
    
    async def delete_connection(self, connection_id: str) -> Dict:
        """
        Delete a connection
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Deletion confirmation
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                logger.warning(f"Deleted connection: {connection_id}")
                return {"deleted": True, "connection_id": connection_id}
    
    async def send_ping(self, connection_id: str, comment: Optional[str] = None) -> Dict:
        """
        Send a trust ping to test connection
        
        Args:
            connection_id: Connection ID
            comment: Optional comment
            
        Returns:
            Ping result
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}/send-ping"
        payload = {}
        
        if comment:
            payload["comment"] = comment
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.debug(f"Sent ping to connection: {connection_id}")
                return result
    
    async def get_connection_metadata(self, connection_id: str) -> Dict:
        """
        Get metadata for a connection
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Connection metadata
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}/metadata"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('results', {})
    
    async def set_connection_metadata(
        self,
        connection_id: str,
        metadata: Dict
    ) -> Dict:
        """
        Set metadata for a connection
        
        Args:
            connection_id: Connection ID
            metadata: Metadata dictionary
            
        Returns:
            Updated metadata
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}/metadata"
        payload = {"metadata": metadata}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Set metadata for connection: {connection_id}")
                return result
