"""
Verifier Agent Configuration
Manages credential verification and presentation requests
"""

import os
from typing import Dict, Any

class VerifierConfig:
    """Configuration for Verifier Agent"""
    
    # Agent Identity
    AGENT_NAME = os.getenv("AGENT_NAME", "verifier-agent")
    AGENT_PORT = int(os.getenv("AGENT_PORT", 8040))
    ADMIN_PORT = int(os.getenv("ADMIN_PORT", 8050))
    
    # Security
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")
    WALLET_KEY = os.getenv("WALLET_KEY", "")
    
    # Wallet Configuration
    WALLET_NAME = os.getenv("WALLET_NAME", "verifier-wallet")
    WALLET_TYPE = os.getenv("WALLET_TYPE", "askar")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # Ledger
    GENESIS_URL = os.getenv("GENESIS_URL", "http://indy-pool:8000/genesis")
    POOL_NAME = os.getenv("POOL_NAME", "local_pool")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
    
    # Auto-behaviors
    AUTO_VERIFY_PRESENTATION = os.getenv("AUTO_VERIFY_PRESENTATION", "true").lower() == "true"
    
    # IPFS Configuration
    IPFS_API_URL = os.getenv("IPFS_API_URL", "http://ipfs:5001")
    IPFS_GATEWAY_URL = os.getenv("IPFS_GATEWAY_URL", "http://ipfs:8080")
    
    @classmethod
    def get_aca_py_args(cls) -> list:
        """Generate ACA-Py startup arguments"""
        return [
            "aca-py", "start",
            "--inbound-transport", "http", "0.0.0.0", str(cls.AGENT_PORT),
            "--outbound-transport", "http",
            "--admin", "0.0.0.0", str(cls.ADMIN_PORT),
            "--admin-api-key", cls.ADMIN_API_KEY,
            "--wallet-type", cls.WALLET_TYPE,
            "--wallet-name", cls.WALLET_NAME,
            "--wallet-key", cls.WALLET_KEY,
            "--genesis-url", cls.GENESIS_URL,
            "--endpoint", f"http://verifier-agent:{cls.AGENT_PORT}",
            "--label", cls.AGENT_NAME,
            "--public-invites",
            "--auto-provision",
            "--auto-ping-connection",
            "--monitor-ping",
            "--auto-verify-presentation",
            "--log-level", cls.LOG_LEVEL,
        ]
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            "agent_name": cls.AGENT_NAME,
            "agent_port": cls.AGENT_PORT,
            "admin_port": cls.ADMIN_PORT,
            "wallet_name": cls.WALLET_NAME,
            "wallet_type": cls.WALLET_TYPE,
            "genesis_url": cls.GENESIS_URL,
            "log_level": cls.LOG_LEVEL,
        }

# Export configuration instance
config = VerifierConfig()
