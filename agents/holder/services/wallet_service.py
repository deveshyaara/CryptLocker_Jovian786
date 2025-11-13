"""
Wallet Service
Manages holder wallet operations including DID creation and credential storage
"""

import logging
from typing import Dict, List, Optional, Any
import aiohttp
from config.agent_config import config

logger = logging.getLogger(__name__)


class WalletService:
    """Service for managing holder wallet operations"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Wallet Service
        
        Args:
            admin_url: ACA-Py admin API URL
            api_key: Admin API key for authentication
        """
        self.admin_url = admin_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key}
    
    async def create_did(self) -> Dict[str, Any]:
        """
        Create a new DID for the holder
        
        Returns:
            DID creation result with DID and verkey
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/wallet/did/create"
                
                async with session.post(url, headers=self.headers, json={}) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Created DID: {result.get('result', {}).get('did')}")
                        return result.get("result", {})
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to create DID: {error_text}")
                        raise Exception(f"DID creation failed: {error_text}")
                        
        except Exception as e:
            logger.error(f"Error creating DID: {str(e)}")
            raise
    
    async def get_public_did(self) -> Optional[Dict[str, Any]]:
        """
        Get the public DID for this wallet
        
        Returns:
            Public DID information or None
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/wallet/did/public"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("result")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting public DID: {str(e)}")
            return None
    
    async def list_dids(self) -> List[Dict[str, Any]]:
        """
        List all DIDs in the wallet
        
        Returns:
            List of DID information
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/wallet/did"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    return []
                    
        except Exception as e:
            logger.error(f"Error listing DIDs: {str(e)}")
            return []
    
    async def get_credentials(self) -> List[Dict[str, Any]]:
        """
        Get all credentials stored in the wallet
        
        Returns:
            List of credential records
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/credentials"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting credentials: {str(e)}")
            return []
    
    async def get_credential_by_id(self, credential_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific credential by ID
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Credential information or None
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/credential/{credential_id}"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting credential {credential_id}: {str(e)}")
            return None
    
    async def delete_credential(self, credential_id: str) -> bool:
        """
        Delete a credential from the wallet
        
        Args:
            credential_id: Credential ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/credential/{credential_id}"
                
                async with session.delete(url, headers=self.headers) as response:
                    if response.status == 200:
                        logger.info(f"Deleted credential: {credential_id}")
                        return True
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting credential {credential_id}: {str(e)}")
            return False
    
    async def get_wallet_info(self) -> Dict[str, Any]:
        """
        Get wallet information
        
        Returns:
            Wallet information
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/status"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting wallet info: {str(e)}")
            return {}
