"""
Connection Model
Represents DIDComm connections between holder and other agents
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class ConnectionState(str, Enum):
    """Connection state enumeration"""
    INVITATION = "invitation"
    REQUEST = "request"
    RESPONSE = "response"
    ACTIVE = "active"
    ERROR = "error"
    COMPLETED = "completed"


class ConnectionBase(BaseModel):
    """Base connection model"""
    alias: Optional[str] = Field(None, max_length=255)
    their_label: Optional[str] = None


class ConnectionCreate(BaseModel):
    """Connection creation from invitation"""
    invitation_url: str


class ConnectionInvitation(BaseModel):
    """Connection invitation model"""
    invitation: dict
    invitation_url: str
    connection_id: str


class Connection(ConnectionBase):
    """Complete connection model"""
    id: int
    user_id: int
    connection_id: str
    state: ConnectionState
    their_did: Optional[str] = None
    my_did: Optional[str] = None
    invitation_key: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConnectionList(BaseModel):
    """List of connections"""
    connections: list[Connection]
    total: int
