"""
Credential Model
Represents a Verifiable Credential stored in the holder's wallet
"""

from datetime import datetime
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class CredentialBase(BaseModel):
    """Base credential model"""
    schema_id: str
    cred_def_id: str
    issuer_did: str
    attributes: Dict[str, Any]


class CredentialStored(CredentialBase):
    """Stored credential model"""
    id: int
    user_id: int
    credential_id: str
    referent: str
    rev_reg_id: Optional[str] = None
    cred_rev_id: Optional[str] = None
    ipfs_hash: Optional[str] = None
    is_revoked: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CredentialOffer(BaseModel):
    """Credential offer from issuer"""
    connection_id: str
    credential_offer: Dict[str, Any]
    credential_preview: Dict[str, Any]
    auto_issue: bool = True


class CredentialRequest(BaseModel):
    """Credential request model"""
    connection_id: str
    credential_offer: Dict[str, Any]


class CredentialList(BaseModel):
    """List of credentials"""
    credentials: list[CredentialStored]
    total: int
    page: int
    page_size: int
