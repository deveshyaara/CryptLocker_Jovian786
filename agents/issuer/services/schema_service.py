"""
Schema Service for Issuer Agent
Manages credential schemas on Indy ledger
"""

import logging
from typing import Dict, List
import aiohttp

logger = logging.getLogger(__name__)


class SchemaService:
    """Service for managing credential schemas"""
    
    def __init__(self, admin_url: str, api_key: str):
        """
        Initialize Schema Service
        
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
    
    async def create_schema(
        self,
        name: str,
        version: str,
        attributes: List[str]
    ) -> Dict:
        """
        Create and publish a new credential schema to the ledger
        
        Args:
            name: Schema name (e.g., "university-degree")
            version: Schema version (e.g., "1.0")
            attributes: List of attribute names (e.g., ["name", "degree", "university"])
            
        Returns:
            Schema information including schema_id
            
        Example:
            {
                "schema_id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
                "schema": {
                    "name": "university-degree",
                    "version": "1.0",
                    "attrNames": ["name", "degree", "university"],
                    "id": "Th7MpTaRZVRYnPiabds81Y:2:university-degree:1.0",
                    "ver": "1.0"
                }
            }
        """
        if not attributes:
            raise ValueError("Schema must have at least one attribute")
        
        endpoint = f"{self.admin_url}/schemas"
        payload = {
            "schema_name": name,
            "schema_version": version,
            "attributes": attributes
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    schema_id = result.get('schema_id') or result.get('sent', {}).get('schema_id')
                    logger.info(f"Created schema: {schema_id}")
                    return result
                else:
                    error = await response.text()
                    logger.error(f"Failed to create schema: {error}")
                    raise Exception(f"Schema creation failed: {error}")
    
    async def get_schema(self, schema_id: str) -> Dict:
        """
        Retrieve a schema from the ledger
        
        Args:
            schema_id: Schema identifier
            
        Returns:
            Schema details
        """
        endpoint = f"{self.admin_url}/schemas/{schema_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('schema', result)
    
    async def list_created_schemas(self) -> List[Dict]:
        """
        List all schemas created by this agent
        
        Returns:
            List of schema IDs created by this issuer
        """
        endpoint = f"{self.admin_url}/schemas/created"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('schema_ids', [])
    
    async def create_credential_definition(
        self,
        schema_id: str,
        tag: str = "default",
        support_revocation: bool = True
    ) -> Dict:
        """
        Create a credential definition for a schema
        
        Args:
            schema_id: Schema identifier
            tag: Tag for this credential definition (default: "default")
            support_revocation: Enable revocation support
            
        Returns:
            Credential definition including cred_def_id
            
        Example:
            {
                "credential_definition_id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default",
                "credential_definition": {
                    "id": "Th7MpTaRZVRYnPiabds81Y:3:CL:127:default",
                    "schemaId": "127",
                    "type": "CL",
                    "tag": "default",
                    "value": {...}
                }
            }
        """
        endpoint = f"{self.admin_url}/credential-definitions"
        payload = {
            "schema_id": schema_id,
            "tag": tag,
            "support_revocation": support_revocation,
            "revocation_registry_size": 1000 if support_revocation else None
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    cred_def_id = result.get('credential_definition_id') or \
                                  result.get('sent', {}).get('credential_definition_id')
                    logger.info(f"Created credential definition: {cred_def_id}")
                    return result
                else:
                    error = await response.text()
                    logger.error(f"Failed to create credential definition: {error}")
                    raise Exception(f"Credential definition creation failed: {error}")
    
    async def get_credential_definition(self, cred_def_id: str) -> Dict:
        """
        Retrieve a credential definition from the ledger
        
        Args:
            cred_def_id: Credential definition identifier
            
        Returns:
            Credential definition details
        """
        endpoint = f"{self.admin_url}/credential-definitions/{cred_def_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('credential_definition', result)
    
    async def list_created_credential_definitions(self) -> List[str]:
        """
        List all credential definitions created by this agent
        
        Returns:
            List of credential definition IDs
        """
        endpoint = f"{self.admin_url}/credential-definitions/created"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                endpoint,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get('credential_definition_ids', [])
