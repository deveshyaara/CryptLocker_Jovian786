"""
Holder Agent Configuration
Centralized configuration management for the Holder Agent
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class HolderConfig:
    """Holder Agent Configuration"""
    
    # Agent Identity
    AGENT_NAME: str = os.getenv("AGENT_NAME", "Digital Wallet Holder")
    AGENT_PORT: int = int(os.getenv("AGENT_PORT", "8060"))
    ADMIN_PORT: int = int(os.getenv("ADMIN_PORT", "8070"))
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "holder-api-key-change-me")
    
    # Wallet Configuration
    WALLET_NAME: str = os.getenv("WALLET_NAME", "holder-wallet")
    WALLET_KEY: str = os.getenv("WALLET_KEY", "holder-wallet-key-change-me")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgres://postgres:postgres123@localhost:5432/wallet_db"
    )
    
    # Ledger Configuration
    GENESIS_URL: str = os.getenv("GENESIS_URL", "http://localhost:9000/genesis")
    
    # IPFS Configuration
    IPFS_API_URL: str = os.getenv("IPFS_API_URL", "http://localhost:5001")
    IPFS_GATEWAY_URL: str = os.getenv("IPFS_GATEWAY_URL", "http://localhost:8080")
    
    # Security Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-key-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Password Hashing
    BCRYPT_ROUNDS: int = 12
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8002"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MESSAGE_QUEUE_SIZE: int = 100


# Global configuration instance
config = HolderConfig()
