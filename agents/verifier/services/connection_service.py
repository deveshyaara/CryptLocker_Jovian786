"""
Connection Service for Verifier Agent
Manages DIDComm connections with holders
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
        state: Optional[str] = None
    ) -> List[Dict]:
        """
        List connections
        
        Args:
            alias: Filter by alias
            state: Filter by state (e.g., "active", "invitation", "request")
            
        Returns:
            List of connection records
        """
        endpoint = f"{self.admin_url}/connections"
        params = {}
        
        if alias:
            params["alias"] = alias
        if state:
            params["state"] = state
        
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
    
    async def send_ping(self, connection_id: str) -> Dict:
        """
        Send a trust ping to test connection
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Ping result
        """
        endpoint = f"{self.admin_url}/connections/{connection_id}/send-ping"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.debug(f"Sent ping to connection: {connection_id}")
                return result
