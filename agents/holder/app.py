"""
Holder Agent Main Application
FastAPI application exposing holder wallet capabilities
"""

import logging
import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm

from config.agent_config import config
from services.auth_service import AuthService
from services.wallet_service import WalletService
from services.connection_service import ConnectionService
from services.credential_service import CredentialService
from services.database_service import db_service
from models.user import User, UserCreate, UserLogin, Token
from models.connection import ConnectionCreate, Connection
from models.credential import CredentialStored

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Holder Agent API",
    description="Decentralized Identity Holder Wallet API",
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

# Security
security = HTTPBearer()

# Admin URL for ACA-Py
ADMIN_HOST = os.getenv("ACAPY_ADMIN_HOST", "localhost")
ADMIN_URL = f"http://{ADMIN_HOST}:{config.ADMIN_PORT}"

# Service instances
auth_service = AuthService()
wallet_service = WalletService(ADMIN_URL, config.ADMIN_API_KEY)
connection_service = ConnectionService(ADMIN_URL, config.ADMIN_API_KEY)
credential_service = CredentialService(ADMIN_URL, config.ADMIN_API_KEY)


# ==================== Dependencies ====================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Verify JWT token and get current user
    
    Args:
        credentials: HTTP bearer credentials
        
    Returns:
        Current user data
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    user_data = auth_service.extract_user_from_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return user_data


# ==================== Health Check ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Holder Agent",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# ==================== Authentication Endpoints ====================

@app.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user
    
    Args:
        user_data: User registration data
        
    Returns:
        JWT token and user information
    """
    # Hash password
    hashed_password = auth_service.hash_password(user_data.password)
    
    # Create DID for user
    try:
        did_result = await wallet_service.create_did()
        did = did_result.get("did")
    except Exception as e:
        logger.error(f"Failed to create DID: {str(e)}")
        did = None
    
    # Create user in database
    try:
        user = await db_service.create_user(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            did=did
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"User creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    # Create JWT token
    token = auth_service.create_access_token(user["id"], user["username"])
    
    # Remove sensitive data
    user_response = {k: v for k, v in user.items() if k != "hashed_password"}
    
    logger.info(f"User registered: {user_data.username}")
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response
    }


@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login
    
    Args:
        form_data: OAuth2 form data (username and password)
        
    Returns:
        JWT token and user information
    """
    # Find user in database
    user = await db_service.get_user_by_username(form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not auth_service.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Check if user is active
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create JWT token
    token = auth_service.create_access_token(user["id"], user["username"])
    
    # Remove sensitive data
    user_response = {k: v for k, v in user.items() if k != "hashed_password"}
    
    logger.info(f"User logged in: {form_data.username}")
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response
    }


@app.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """
    Get current user information
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    user_id = current_user["user_id"]
    user = await db_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Remove sensitive data
    user_response = {k: v for k, v in user.items() if k != "hashed_password"}
    return user_response


# ==================== Wallet Endpoints ====================

@app.get("/wallet/did")
async def get_wallet_did(current_user: Dict = Depends(get_current_user)):
    """
    Get wallet DID
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        DID information
    """
    user_id = current_user["user_id"]
    user = await db_service.get_user_by_id(user_id)
    
    if not user or not user.get("did"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DID not found for user"
        )
    
    return {
        "did": user["did"],
        "wallet_id": user.get("wallet_id")
    }


@app.get("/wallet/info")
async def get_wallet_info(current_user: Dict = Depends(get_current_user)):
    """
    Get wallet information
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Wallet information
    """
    wallet_info = await wallet_service.get_wallet_info()
    return wallet_info


# ==================== Connection Endpoints ====================

@app.post("/connections", status_code=status.HTTP_201_CREATED)
async def receive_invitation(
    invitation: ConnectionCreate,
    current_user: Dict = Depends(get_current_user)
):
    """
    Receive and accept a connection invitation
    
    Args:
        invitation: Connection invitation
        current_user: Current authenticated user
        
    Returns:
        Connection record
    """
    try:
        connection = await connection_service.receive_invitation(
            invitation.invitation_url
        )
        return connection
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/connections")
async def list_connections(
    state: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    List all connections
    
    Args:
        state: Optional state filter
        current_user: Current authenticated user
        
    Returns:
        List of connections
    """
    connections = await connection_service.list_connections(state)
    return {
        "connections": connections,
        "total": len(connections)
    }


@app.get("/connections/{connection_id}")
async def get_connection(
    connection_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get a specific connection
    
    Args:
        connection_id: Connection ID
        current_user: Current authenticated user
        
    Returns:
        Connection record
    """
    connection = await connection_service.get_connection(connection_id)
    
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    
    return connection


@app.delete("/connections/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(
    connection_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete a connection
    
    Args:
        connection_id: Connection ID
        current_user: Current authenticated user
    """
    success = await connection_service.delete_connection(connection_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )


# ==================== Credential Endpoints ====================

@app.get("/credentials")
async def list_credentials(current_user: Dict = Depends(get_current_user)):
    """
    List all stored credentials
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of credentials
    """
    credentials = await credential_service.get_credentials()
    return {
        "credentials": credentials,
        "total": len(credentials)
    }


@app.get("/credentials/{credential_id}")
async def get_credential(
    credential_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get a specific credential
    
    Args:
        credential_id: Credential ID
        current_user: Current authenticated user
        
    Returns:
        Credential record
    """
    credential = await credential_service.get_credential(credential_id)
    
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found"
        )
    
    return credential


@app.delete("/credentials/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credential(
    credential_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete a credential
    
    Args:
        credential_id: Credential ID
        current_user: Current authenticated user
    """
    success = await credential_service.delete_credential(credential_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found"
        )


@app.get("/credentials/offers")
async def list_credential_offers(current_user: Dict = Depends(get_current_user)):
    """
    List pending credential offers
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of credential offers
    """
    offers = await credential_service.get_credential_offers()
    return {
        "offers": offers,
        "total": len(offers)
    }


@app.post("/credentials/offers/{credential_exchange_id}/accept")
async def accept_credential_offer(
    credential_exchange_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Accept a credential offer
    
    Args:
        credential_exchange_id: Credential exchange ID
        current_user: Current authenticated user
        
    Returns:
        Updated credential exchange record
    """
    try:
        # Send credential request
        result = await credential_service.request_credential(credential_exchange_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/proofs/requests")
async def list_proof_requests(current_user: Dict = Depends(get_current_user)):
    """
    List pending proof requests
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of proof requests
    """
    requests = await credential_service.get_proof_requests()
    return {
        "proof_requests": requests,
        "total": len(requests)
    }


# ==================== Error Handlers ====================

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle generic exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "detail": "Internal server error",
        "error": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level=config.LOG_LEVEL.lower()
    )
