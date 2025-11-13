"""
Credential Service
Manages credential operations for the holder
"""

import logging
from typing import Dict, List, Optional, Any
import aiohttp
from config.agent_config import config

logger = logging.getLogger(__name__)


class CredentialService:
    """Service for managing holder credentials"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Credential Service
        
        Args:
            admin_url: ACA-Py admin API URL
            api_key: Admin API key for authentication
        """
        self.admin_url = admin_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key}
    
    async def get_credential_offers(self) -> List[Dict[str, Any]]:
        """
        Get all credential offers
        
        Returns:
            List of credential offer records
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/issue-credential/records"
                params = {"state": "offer_received"}
                
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting credential offers: {str(e)}")
            return []
    
    async def request_credential(self, credential_exchange_id: str) -> Dict[str, Any]:
        """
        Send credential request for an offer
        
        Args:
            credential_exchange_id: Credential exchange ID
            
        Returns:
            Updated credential exchange record
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/issue-credential/records/{credential_exchange_id}/send-request"
                
                async with session.post(url, headers=self.headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Sent credential request: {credential_exchange_id}")
                        return result
                    else:
                        error_text = await response.text()
                        raise Exception(f"Credential request failed: {error_text}")
                        
        except Exception as e:
            logger.error(f"Error requesting credential {credential_exchange_id}: {str(e)}")
            raise
    
    async def store_credential(self, credential_exchange_id: str, credential_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Store a received credential in the wallet
        
        Args:
            credential_exchange_id: Credential exchange ID
            credential_id: Optional credential ID for the stored credential
            
        Returns:
            Updated credential exchange record
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/issue-credential/records/{credential_exchange_id}/store"
                
                payload = {}
                if credential_id:
                    payload["credential_id"] = credential_id
                
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Stored credential: {credential_exchange_id}")
                        return result
                    else:
                        error_text = await response.text()
                        raise Exception(f"Credential storage failed: {error_text}")
                        
        except Exception as e:
            logger.error(f"Error storing credential {credential_exchange_id}: {str(e)}")
            raise
    
    async def get_credentials(self, wql: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get stored credentials from wallet
        
        Args:
            wql: Optional WQL (Wallet Query Language) filter
            
        Returns:
            List of credential records
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/credentials"
                
                params = {}
                if wql:
                    params["wql"] = wql
                
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting credentials: {str(e)}")
            return []
    
    async def get_credential(self, credential_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific credential
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Credential record or None
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
            credential_id: Credential ID
            
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
    
    async def create_proof_presentation(
        self,
        proof_request: Dict[str, Any],
        requested_credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a proof presentation from credentials
        
        Args:
            proof_request: Proof request from verifier
            requested_credentials: Credentials to use in presentation
            
        Returns:
            Proof presentation
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/present-proof/records/{proof_request['pres_ex_id']}/send-presentation"
                
                async with session.post(url, headers=self.headers, json=requested_credentials) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Created proof presentation: {proof_request['pres_ex_id']}")
                        return result
                    else:
                        error_text = await response.text()
                        raise Exception(f"Proof presentation failed: {error_text}")
                        
        except Exception as e:
            logger.error(f"Error creating proof presentation: {str(e)}")
            raise
    
    async def get_proof_requests(self) -> List[Dict[str, Any]]:
        """
        Get all proof requests
        
        Returns:
            List of proof request records
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.admin_url}/present-proof/records"
                params = {"state": "request_received"}
                
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting proof requests: {str(e)}")
            return []
