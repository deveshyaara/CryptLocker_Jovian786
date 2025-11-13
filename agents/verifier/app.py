"""
Verifier Agent Main Application
FastAPI application exposing verifier capabilities
"""

import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config.agent_config import config
from .services.presentation_service import PresentationService
from .services.connection_service import ConnectionService

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Verifier Agent API",
    description="Decentralized Identity Credential Verification API",
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

# Admin URL for ACA-Py - Use environment variable or default to localhost
import os
ADMIN_HOST = os.getenv("ACAPY_ADMIN_HOST", "localhost")
ADMIN_URL = f"http://{ADMIN_HOST}:{config.ADMIN_PORT}"

# Service instances
presentation_service = PresentationService(ADMIN_URL, config.ADMIN_API_KEY)
connection_service = ConnectionService(ADMIN_URL, config.ADMIN_API_KEY)


# ==================== Request/Response Models ====================

class RequestedAttribute(BaseModel):
    name: str
    restrictions: Optional[List[Dict]] = None


class RequestedPredicate(BaseModel):
    name: str
    p_type: str = Field(..., description="Predicate type: >=, <=, >, <")
    p_value: int
    restrictions: Optional[List[Dict]] = None


class ProofRequestPayload(BaseModel):
    connection_id: str
    name: str
    version: str = "1.0"
    requested_attributes: Dict[str, RequestedAttribute]
    requested_predicates: Optional[Dict[str, RequestedPredicate]] = None
    comment: Optional[str] = None


class CreateInvitationRequest(BaseModel):
    alias: Optional[str] = None
    multi_use: bool = False
    public: bool = False


# ==================== Health Check ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Verifier Agent",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
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


# ==================== Proof Request Management ====================

@app.post("/proof-requests/send")
async def send_proof_request(request: ProofRequestPayload):
    """Send a proof request to a holder"""
    try:
        # Convert Pydantic models to dictionaries
        requested_attributes = {}
        for key, attr in request.requested_attributes.items():
            requested_attributes[key] = {
                "name": attr.name
            }
            if attr.restrictions:
                requested_attributes[key]["restrictions"] = attr.restrictions
        
        requested_predicates = {}
        if request.requested_predicates:
            for key, pred in request.requested_predicates.items():
                requested_predicates[key] = {
                    "name": pred.name,
                    "p_type": pred.p_type,
                    "p_value": pred.p_value
                }
                if pred.restrictions:
                    requested_predicates[key]["restrictions"] = pred.restrictions
        
        # Create proof request
        proof_request = await presentation_service.create_proof_request(
            name=request.name,
            version=request.version,
            requested_attributes=requested_attributes,
            requested_predicates=requested_predicates if requested_predicates else None
        )
        
        # Send proof request
        result = await presentation_service.send_proof_request(
            connection_id=request.connection_id,
            proof_request=proof_request,
            comment=request.comment
        )
        
        return result
    except Exception as e:
        logger.error(f"Failed to send proof request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/proof-requests/exchanges")
async def list_presentation_exchanges(
    connection_id: Optional[str] = None,
    state: Optional[str] = None
):
    """List presentation exchange records"""
    try:
        result = await presentation_service.list_presentation_exchanges(
            connection_id=connection_id,
            state=state
        )
        return {"results": result}
    except Exception as e:
        logger.error(f"Failed to list presentation exchanges: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/proof-requests/exchanges/{presentation_exchange_id}")
async def get_presentation_exchange(presentation_exchange_id: str):
    """Get presentation exchange record details"""
    try:
        result = await presentation_service.get_presentation_exchange_record(
            presentation_exchange_id
        )
        return result
    except Exception as e:
        logger.error(f"Failed to get presentation exchange: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/proof-requests/exchanges/{presentation_exchange_id}/verify")
async def verify_presentation(presentation_exchange_id: str):
    """Verify a received presentation"""
    try:
        result = await presentation_service.verify_presentation(
            presentation_exchange_id
        )
        return result
    except Exception as e:
        logger.error(f"Failed to verify presentation: {e}")
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
