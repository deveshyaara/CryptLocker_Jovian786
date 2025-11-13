"""
Presentation Service for Verifier Agent
Handles proof requests and verification
"""

import logging
from typing import Dict, List, Optional
import aiohttp

logger = logging.getLogger(__name__)


class PresentationService:
    """Service for requesting and verifying presentations"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Presentation Service
        
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
    
    async def send_proof_request(
        self,
        connection_id: str,
        proof_request: Dict,
        comment: Optional[str] = None
    ) -> Dict:
        """
        Send a proof request to a holder
        
        Args:
            connection_id: Connection ID with the holder
            proof_request: Proof request specification
            comment: Optional comment
            
        Returns:
            Presentation exchange record
            
        Example proof_request:
            {
                "name": "Proof of Education",
                "version": "1.0",
                "requested_attributes": {
                    "attr1_referent": {
                        "name": "degree",
                        "restrictions": [
                            {
                                "cred_def_id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default"
                            }
                        ]
                    }
                },
                "requested_predicates": {
                    "pred1_referent": {
                        "name": "graduation_year",
                        "p_type": ">=",
                        "p_value": 2020,
                        "restrictions": [
                            {
                                "cred_def_id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default"
                            }
                        ]
                    }
                }
            }
        """
        endpoint = f"{self.admin_url}/present-proof/send-request"
        payload = {
            "connection_id": connection_id,
            "proof_request": proof_request,
            "auto_verify": True,
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
                logger.info(f"Sent proof request: {result.get('presentation_exchange_id')}")
                return result
    
    async def verify_presentation(self, presentation_exchange_id: str) -> Dict:
        """
        Verify a received presentation
        
        Args:
            presentation_exchange_id: Presentation exchange record ID
            
        Returns:
            Verification result
        """
        endpoint = f"{self.admin_url}/present-proof/records/{presentation_exchange_id}/verify-presentation"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Verified presentation: {presentation_exchange_id}")
                return result
    
    async def get_presentation_exchange_record(self, presentation_exchange_id: str) -> Dict:
        """
        Get presentation exchange record details
        
        Args:
            presentation_exchange_id: Exchange record ID
            
        Returns:
            Presentation exchange record with verification status
        """
        endpoint = f"{self.admin_url}/present-proof/records/{presentation_exchange_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def list_presentation_exchanges(
        self,
        connection_id: Optional[str] = None,
        state: Optional[str] = None
    ) -> List[Dict]:
        """
        List presentation exchange records
        
        Args:
            connection_id: Filter by connection ID
            state: Filter by state (e.g., "request_sent", "presentation_received", "verified")
            
        Returns:
            List of presentation exchange records
        """
        endpoint = f"{self.admin_url}/present-proof/records"
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
    
    async def create_proof_request(
        self,
        name: str,
        version: str,
        requested_attributes: Dict,
        requested_predicates: Optional[Dict] = None,
        non_revoked: Optional[Dict] = None
    ) -> Dict:
        """
        Create a proof request structure
        
        Args:
            name: Proof request name
            version: Proof request version
            requested_attributes: Dictionary of requested attributes
            requested_predicates: Dictionary of requested predicates (optional)
            non_revoked: Non-revocation interval (optional)
            
        Returns:
            Proof request object
            
        Example:
            requested_attributes = {
                "attr1_referent": {
                    "name": "name",
                    "restrictions": [{"cred_def_id": "..."}]
                }
            }
            
            requested_predicates = {
                "pred1_referent": {
                    "name": "age",
                    "p_type": ">=",
                    "p_value": 18,
                    "restrictions": [{"cred_def_id": "..."}]
                }
            }
        """
        proof_request = {
            "name": name,
            "version": version,
            "requested_attributes": requested_attributes,
            "requested_predicates": requested_predicates or {}
        }
        
        if non_revoked:
            proof_request["non_revoked"] = non_revoked
        
        return proof_request
    
    async def get_credentials_for_presentation(
        self,
        presentation_exchange_id: str
    ) -> Dict:
        """
        Get credentials available for a presentation request
        
        Args:
            presentation_exchange_id: Presentation exchange record ID
            
        Returns:
            Available credentials that satisfy the proof request
        """
        endpoint = f"{self.admin_url}/present-proof/records/{presentation_exchange_id}/credentials"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def send_presentation(
        self,
        presentation_exchange_id: str,
        requested_credentials: Dict
    ) -> Dict:
        """
        Send presentation as a holder (for testing)
        
        Args:
            presentation_exchange_id: Presentation exchange record ID
            requested_credentials: Credentials to use in the presentation
            
        Returns:
            Updated presentation exchange record
        """
        endpoint = f"{self.admin_url}/present-proof/records/{presentation_exchange_id}/send-presentation"
        payload = {
            "requested_credentials": requested_credentials
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Sent presentation: {presentation_exchange_id}")
                return result
    
    async def delete_presentation_exchange(self, presentation_exchange_id: str) -> Dict:
        """
        Delete a presentation exchange record
        
        Args:
            presentation_exchange_id: Exchange record ID
            
        Returns:
            Deletion confirmation
        """
        endpoint = f"{self.admin_url}/present-proof/records/{presentation_exchange_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                logger.info(f"Deleted presentation exchange: {presentation_exchange_id}")
                return {"deleted": True, "presentation_exchange_id": presentation_exchange_id}
