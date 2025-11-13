"""
Authentication Service
Handles user registration, login, and JWT token management
"""

import logging
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import jwt
from config.agent_config import config

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for user management"""
    
    def __init__(self):
        """Initialize authentication service"""
        self.secret_key = config.JWT_SECRET_KEY
        self.algorithm = config.JWT_ALGORITHM
        self.expiration_hours = config.JWT_EXPIRATION_HOURS
        self.bcrypt_rounds = config.BCRYPT_ROUNDS
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        # Bcrypt has a 72-byte limit, truncate if necessary
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            # Bcrypt has a 72-byte limit
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, user_id: int, username: str) -> str:
        """
        Create a JWT access token
        
        Args:
            user_id: User ID
            username: Username
            
        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(hours=self.expiration_hours)
        
        payload = {
            "user_id": user_id,
            "username": username,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        logger.info(f"Created access token for user: {username}")
        
        return token
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify and decode a JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
            
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def extract_user_from_token(self, token: str) -> Optional[dict]:
        """
        Extract user information from token
        
        Args:
            token: JWT token string
            
        Returns:
            User data dict or None if invalid
        """
        payload = self.verify_token(token)
        
        if payload:
            return {
                "user_id": payload.get("user_id"),
                "username": payload.get("username")
            }
        
        return None
