"""
Connection Service
Manages DIDComm connections between holder and other agents
"""

import logging
from typing import Dict, List, Optional, Any
import aiohttp
from config.agent_config import config

logger = logging.getLogger(__name__)


class ConnectionService:
    """Service for managing holder connections"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Connection Service
        
        Args:
            admin_url: ACA-Py admin API URL
            api_key: Admin API key for authentication
        """
        self.admin_url = admin_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key}
    
    async def receive_invitation(self, invitation_url: str, alias: Optional[str] = None) -> Dict[str, Any]:
        """
        Receive and accept a connection invitation
        
        Args:
            invitation_url: Connection invitation URL
            alias: Optional alias for the connection
            
        Returns:
            Connection record
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/connections/receive-invitation"
                
                params = {
                    "auto_accept": "true"
                }
                if alias:
                    params["alias"] = alias
                
                # Parse invitation from URL
                invitation_data = self._parse_invitation_url(invitation_url)
                
                async with session.post(
                    url,
                    headers=self.headers,
                    json=invitation_data,
                    params=params
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Received invitation: {result.get('connection_id')}")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to receive invitation: {error_text}")
                        raise Exception(f"Invitation receive failed: {error_text}")
                        
        except Exception as e:
            logger.error(f"Error receiving invitation: {str(e)}")
            raise
    
    async def list_connections(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all connections
        
        Args:
            state: Optional state filter (active, invitation, etc.)
            
        Returns:
            List of connection records
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/connections"
                
                params = {}
                if state:
                    params["state"] = state
                
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    return []
                    
        except Exception as e:
            logger.error(f"Error listing connections: {str(e)}")
            return []
    
    async def get_connection(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific connection by ID
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Connection record or None
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/connections/{connection_id}"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting connection {connection_id}: {str(e)}")
            return None
    
    async def delete_connection(self, connection_id: str) -> bool:
        """
        Delete a connection
        
        Args:
            connection_id: Connection ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/connections/{connection_id}"
                
                async with session.delete(url, headers=self.headers) as response:
                    if response.status == 200:
                        logger.info(f"Deleted connection: {connection_id}")
                        return True
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting connection {connection_id}: {str(e)}")
            return False
    
    async def accept_invitation(self, connection_id: str) -> Dict[str, Any]:
        """
        Accept a connection invitation
        
        Args:
            connection_id: Connection ID
            
        Returns:
            Updated connection record
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/connections/{connection_id}/accept-invitation"
                
                async with session.post(url, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Accepted invitation: {connection_id}")
                        return result
                    else:
                        error_text = await response.text()
                        raise Exception(f"Failed to accept invitation: {error_text}")
                        
        except Exception as e:
            logger.error(f"Error accepting invitation {connection_id}: {str(e)}")
            raise
    
    def _parse_invitation_url(self, invitation_url: str) -> Dict[str, Any]:
        """
        Parse invitation from URL
        
        Args:
            invitation_url: Invitation URL string
            
        Returns:
            Parsed invitation data
        """
        import json
        import base64
        from urllib.parse import urlparse, parse_qs
        
        try:
            # Parse URL
            parsed = urlparse(invitation_url)
            query_params = parse_qs(parsed.query)
            
            # Get invitation parameter
            if 'c_i' in query_params:
                # Base64 encoded invitation
                encoded = query_params['c_i'][0]
                decoded = base64.b64decode(encoded)
                return json.loads(decoded)
            elif 'oob' in query_params:
                # Out-of-band invitation
                encoded = query_params['oob'][0]
                decoded = base64.b64decode(encoded)
                return json.loads(decoded)
            else:
                raise ValueError("Invalid invitation URL format")
                
        except Exception as e:
            logger.error(f"Error parsing invitation URL: {str(e)}")
            raise
