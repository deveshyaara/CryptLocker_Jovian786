"""
Credential Issuance Service
Handles credential offers, issuance, and revocation
"""

import logging
from typing import Dict, List, Optional
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)


class CredentialService:
    """Service for issuing and managing credentials"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Credential Service
        
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
    
    async def send_credential_offer(
        self,
        connection_id: str,
        cred_def_id: str,
        attributes: List[Dict[str, str]],
        comment: Optional[str] = None
    ) -> Dict:
        """
        Send credential offer to a holder
        
        Args:
            connection_id: Connection ID with the holder
            cred_def_id: Credential definition ID
            attributes: List of credential attributes [{"name": "attr", "value": "val"}]
            comment: Optional comment
            
        Returns:
            Credential exchange record
            
        Example attributes:
            [
                {"name": "name", "value": "Alice Smith"},
                {"name": "degree", "value": "Bachelor of Science"},
                {"name": "university", "value": "MIT"},
                {"name": "graduation_date", "value": "2023-06-15"}
            ]
        """
        endpoint = f"{self.admin_url}/issue-credential/send-offer"
        payload = {
            "connection_id": connection_id,
            "cred_def_id": cred_def_id,
            "credential_preview": {
                "@type": "issue-credential/1.0/credential-preview",
                "attributes": attributes
            },
            "auto_issue": False,  # Manual approval for security
            "auto_remove": False,
            "trace": False
        }
        
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
                logger.info(f"Sent credential offer: {result.get('credential_exchange_id')}")
                return result
    
    async def issue_credential(self, credential_exchange_id: str) -> Dict:
        """
        Issue credential after holder accepts the offer
        
        Args:
            credential_exchange_id: Credential exchange record ID
            
        Returns:
            Updated credential exchange record
        """
        endpoint = f"{self.admin_url}/issue-credential/records/{credential_exchange_id}/issue"
        payload = {}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Issued credential: {credential_exchange_id}")
                return result
    
    async def get_credential_exchange_record(self, credential_exchange_id: str) -> Dict:
        """
        Get credential exchange record details
        
        Args:
            credential_exchange_id: Exchange record ID
            
        Returns:
            Credential exchange record
        """
        endpoint = f"{self.admin_url}/issue-credential/records/{credential_exchange_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def list_credential_exchanges(
        self,
        connection_id: Optional[str] = None,
        state: Optional[str] = None
    ) -> List[Dict]:
        """
        List credential exchange records
        
        Args:
            connection_id: Filter by connection ID
            state: Filter by state (e.g., "offer_sent", "credential_issued")
            
        Returns:
            List of credential exchange records
        """
        endpoint = f"{self.admin_url}/issue-credential/records"
        params = {}
        
        if connection_id:
            params["connection_id"] = connection_id
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
    
    async def revoke_credential(
        self,
        rev_reg_id: str,
        cred_rev_id: str,
        publish: bool = True,
        notify: bool = True,
        notify_version: str = "v1_0"
    ) -> Dict:
        """
        Revoke a credential
        
        Args:
            rev_reg_id: Revocation registry ID
            cred_rev_id: Credential revocation ID
            publish: Publish revocation to ledger immediately
            notify: Send revocation notification to holder
            notify_version: Notification protocol version
            
        Returns:
            Revocation result
        """
        endpoint = f"{self.admin_url}/revocation/revoke"
        payload = {
            "rev_reg_id": rev_reg_id,
            "cred_rev_id": cred_rev_id,
            "publish": publish,
            "notify": notify,
            "notify_version": notify_version
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.warning(f"Revoked credential: {cred_rev_id} in registry {rev_reg_id}")
                return result
    
    async def publish_revocations(self, rev_reg_id: str) -> Dict:
        """
        Publish pending revocations to the ledger
        
        Args:
            rev_reg_id: Revocation registry ID
            
        Returns:
            Publication result
        """
        endpoint = f"{self.admin_url}/revocation/publish-revocations"
        payload = {"rrid2crid": {rev_reg_id: []}}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Published revocations for registry: {rev_reg_id}")
                return result
    
    async def get_revocation_status(self, rev_reg_id: str, cred_rev_id: str) -> Dict:
        """
        Check if a credential has been revoked
        
        Args:
            rev_reg_id: Revocation registry ID
            cred_rev_id: Credential revocation ID
            
        Returns:
            Revocation status
        """
        endpoint = f"{self.admin_url}/revocation/credential-record"
        params = {
            "rev_reg_id": rev_reg_id,
            "cred_rev_id": cred_rev_id
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def create_revocation_registry(self, cred_def_id: str, max_cred_num: int = 1000) -> Dict:
        """
        Create a new revocation registry for a credential definition
        
        Args:
            cred_def_id: Credential definition ID
            max_cred_num: Maximum number of credentials in this registry
            
        Returns:
            Revocation registry information
        """
        endpoint = f"{self.admin_url}/revocation/create-registry"
        payload = {
            "credential_definition_id": cred_def_id,
            "max_cred_num": max_cred_num
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Created revocation registry: {result.get('result', {}).get('revoc_reg_id')}")
                return result
