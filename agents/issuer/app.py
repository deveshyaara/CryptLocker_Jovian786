"""
Issuer Agent Main Application
FastAPI application exposing issuer capabilities
"""

import logging
import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config.agent_config import config
from .services.did_service import DIDService
from .services.schema_service import SchemaService
from .services.credential_service import CredentialService
from .services.connection_service import ConnectionService

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Issuer Agent API",
    description="Decentralized Identity Credential Issuance API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin URL for ACA-Py
ADMIN_URL = f"http://localhost:{config.ADMIN_PORT}"

# Service instances
did_service = DIDService(ADMIN_URL, config.ADMIN_API_KEY)
schema_service = SchemaService(ADMIN_URL, config.ADMIN_API_KEY)
credential_service = CredentialService(ADMIN_URL, config.ADMIN_API_KEY)
connection_service = ConnectionService(ADMIN_URL, config.ADMIN_API_KEY)


# ==================== Request/Response Models ====================

class CreateSchemaRequest(BaseModel):
    name: str = Field(..., description="Schema name")
    version: str = Field(..., description="Schema version")
    attributes: List[str] = Field(..., description="List of attribute names")


class CreateCredDefRequest(BaseModel):
    schema_id: str = Field(..., description="Schema identifier")
    tag: str = Field(default="default", description="Credential definition tag")
    support_revocation: bool = Field(default=True, description="Enable revocation")


class CredentialAttribute(BaseModel):
    name: str
    value: str


class IssueCredentialRequest(BaseModel):
    connection_id: str = Field(..., description="Connection ID with holder")
    cred_def_id: str = Field(..., description="Credential definition ID")
    attributes: List[CredentialAttribute] = Field(..., description="Credential attributes")
    comment: Optional[str] = Field(None, description="Optional comment")


class RevokeCredentialRequest(BaseModel):
    rev_reg_id: str = Field(..., description="Revocation registry ID")
    cred_rev_id: str = Field(..., description="Credential revocation ID")
    publish: bool = Field(default=True, description="Publish immediately")
    notify: bool = Field(default=True, description="Notify holder")


class CreateInvitationRequest(BaseModel):
    alias: Optional[str] = Field(None, description="Connection alias")
    multi_use: bool = Field(default=False, description="Allow multiple uses")
    public: bool = Field(default=False, description="Use public DID")


# ==================== Health Check ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Issuer Agent",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if we can reach ACA-Py admin API
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{ADMIN_URL}/status",
                headers={"X-API-Key": config.ADMIN_API_KEY}
            ) as response:
                if response.status == 200:
                    return {"status": "healthy", "acapy": "connected"}
                else:
                    return {"status": "degraded", "acapy": "unreachable"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ==================== DID Management ====================

@app.post("/dids/create")
async def create_did(seed: Optional[str] = None):
    """Create a new DID"""
    try:
        result = await did_service.create_did(seed)
        return result
    except Exception as e:
        logger.error(f"Failed to create DID: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dids/public")
async def get_public_did():
    """Get public DID"""
    try:
        result = await did_service.get_public_did()
        if not result:
            raise HTTPException(status_code=404, detail="No public DID set")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get public DID: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dids")
async def list_dids():
    """List all DIDs"""
    try:
        result = await did_service.list_dids()
        return {"dids": result}
    except Exception as e:
        logger.error(f"Failed to list DIDs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Schema Management ====================

@app.post("/schemas")
async def create_schema(request: CreateSchemaRequest):
    """Create a new credential schema"""
    try:
        result = await schema_service.create_schema(
            name=request.name,
            version=request.version,
            attributes=request.attributes
        )
        return result
    except Exception as e:
        logger.error(f"Failed to create schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schemas/{schema_id}")
async def get_schema(schema_id: str):
    """Get schema by ID"""
    try:
        result = await schema_service.get_schema(schema_id)
        return result
    except Exception as e:
        logger.error(f"Failed to get schema: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/schemas")
async def list_schemas():
    """List created schemas"""
    try:
        result = await schema_service.list_created_schemas()
        return {"schema_ids": result}
    except Exception as e:
        logger.error(f"Failed to list schemas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Credential Definition Management ====================

@app.post("/credential-definitions")
async def create_credential_definition(request: CreateCredDefRequest):
    """Create a credential definition"""
    try:
        result = await schema_service.create_credential_definition(
            schema_id=request.schema_id,
            tag=request.tag,
            support_revocation=request.support_revocation
        )
        return result
    except Exception as e:
        logger.error(f"Failed to create credential definition: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/credential-definitions/{cred_def_id}")
async def get_credential_definition(cred_def_id: str):
    """Get credential definition by ID"""
    try:
        result = await schema_service.get_credential_definition(cred_def_id)
        return result
    except Exception as e:
        logger.error(f"Failed to get credential definition: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/credential-definitions")
async def list_credential_definitions():
    """List created credential definitions"""
    try:
        result = await schema_service.list_created_credential_definitions()
        return {"credential_definition_ids": result}
    except Exception as e:
        logger.error(f"Failed to list credential definitions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Credential Issuance ====================

@app.post("/credentials/issue")
async def issue_credential(request: IssueCredentialRequest):
    """Issue a credential to a holder"""
    try:
        # Convert Pydantic models to dicts
        attributes = [{"name": attr.name, "value": attr.value} for attr in request.attributes]
        
        result = await credential_service.send_credential_offer(
            connection_id=request.connection_id,
            cred_def_id=request.cred_def_id,
            attributes=attributes,
            comment=request.comment
        )
        return result
    except Exception as e:
        logger.error(f"Failed to issue credential: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/credentials/exchanges")
async def list_credential_exchanges(
    connection_id: Optional[str] = None,
    state: Optional[str] = None
):
    """List credential exchange records"""
    try:
        result = await credential_service.list_credential_exchanges(
            connection_id=connection_id,
            state=state
        )
        return {"results": result}
    except Exception as e:
        logger.error(f"Failed to list credential exchanges: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/credentials/revoke")
async def revoke_credential(request: RevokeCredentialRequest):
    """Revoke a credential"""
    try:
        result = await credential_service.revoke_credential(
            rev_reg_id=request.rev_reg_id,
            cred_rev_id=request.cred_rev_id,
            publish=request.publish,
            notify=request.notify
        )
        return result
    except Exception as e:
        logger.error(f"Failed to revoke credential: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Connection Management ====================

@app.post("/connections/create-invitation")
async def create_invitation(request: CreateInvitationRequest):
    """Create a connection invitation"""
    try:
        result = await connection_service.create_invitation(
            alias=request.alias,
            multi_use=request.multi_use,
            public=request.public
        )
        return result
    except Exception as e:
        logger.error(f"Failed to create invitation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/connections")
async def list_connections(
    alias: Optional[str] = None,
    state: Optional[str] = None
):
    """List connections"""
    try:
        result = await connection_service.list_connections(
            alias=alias,
            state=state
        )
        return {"results": result}
    except Exception as e:
        logger.error(f"Failed to list connections: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/connections/{connection_id}")
async def get_connection(connection_id: str):
    """Get connection details"""
    try:
        result = await connection_service.get_connection(connection_id)
        return result
    except Exception as e:
        logger.error(f"Failed to get connection: {e}")
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=config.LOG_LEVEL.lower()
    )
