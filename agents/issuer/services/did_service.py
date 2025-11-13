"""
DID Service for Issuer Agent
Handles DID creation, registration, and resolution
"""

import logging
from typing import Dict, Optional
import aiohttp
from ..config.agent_config import config

logger = logging.getLogger(__name__)


class DIDService:
    """Service for managing Decentralized Identifiers"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize DID Service
        
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
    
    async def create_did(self, seed: Optional[str] = None) -> Dict:
        """
        Create a new DID
        
        Args:
            seed: Optional 32-character seed for deterministic DID generation
            
        Returns:
            Dict containing DID and verification key
            
        Example:
            {
                "did": "did:indy:sovrin:WRfXPg8dantKVubE3HX8pw",
                "verkey": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL",
                "posture": "wallet_only"
            }
        """
        endpoint = f"{self.admin_url}/wallet/did/create"
        payload = {}
        
        if seed:
            if len(seed) != 32:
                raise ValueError("Seed must be exactly 32 characters")
            payload["seed"] = seed
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                
                logger.info(f"Created DID: {result['result']['did']}")
                return result['result']
    
    async def register_did_on_ledger(self, did: str, verkey: str) -> Dict:
        """
        Register DID on Indy ledger (requires Endorser role)
        
        Args:
            did: DID to register
            verkey: Verification key
            
        Returns:
            Registration result
        """
        # In production, this would go through an endorser
        # For development, we use a pre-configured seed with ledger access
        endpoint = f"{self.admin_url}/ledger/register-nym"
        payload = {
            "did": did,
            "verkey": verkey,
            "alias": config.AGENT_NAME,
            "role": "TRUST_ANCHOR"  # Required for issuing credentials
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Registered DID on ledger: {did}")
                    return result
                else:
                    error = await response.text()
                    logger.error(f"Failed to register DID: {error}")
                    raise Exception(f"DID registration failed: {error}")
    
    async def get_public_did(self) -> Optional[Dict]:
        """
        Get the agent's public DID
        
        Returns:
            Public DID information or None if not set
        """
        endpoint = f"{self.admin_url}/wallet/did/public"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('result')
                return None
    
    async def set_public_did(self, did: str) -> Dict:
        """
        Set a DID as the agent's public DID
        
        Args:
            did: DID to set as public
            
        Returns:
            Updated DID information
        """
        endpoint = f"{self.admin_url}/wallet/did/public"
        params = {"did": did}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Set public DID: {did}")
                return result['result']
    
    async def resolve_did(self, did: str) -> Dict:
        """
        Resolve a DID to get its DID Document from the ledger
        
        Args:
            did: DID to resolve
            
        Returns:
            DID Document
        """
        endpoint = f"{self.admin_url}/resolver/resolve/{did}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result
    
    async def list_dids(self) -> list:
        """
        List all DIDs in the wallet
        
        Returns:
            List of DID information
        """
        endpoint = f"{self.admin_url}/wallet/did"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('results', [])
    
    async def rotate_keypair(self, did: str) -> Dict:
        """
        Rotate the keypair for a DID (updates verification key on ledger)
        
        Args:
            did: DID to rotate keys for
            
        Returns:
            New verification key
        """
        endpoint = f"{self.admin_url}/wallet/did/local/rotate-keypair"
        payload = {"did": did}
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.warning(f"Rotated keypair for DID: {did}")
                return result
