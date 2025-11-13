"""
Database Service
Handles PostgreSQL database operations for user management
"""

import logging
from datetime import datetime
from typing import Optional, Dict, List
import psycopg2
from psycopg2.extras import RealDictCursor
from config.agent_config import config

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        """Initialize database service"""
        self.database_url = config.DATABASE_URL
        self._connection = None
    
    def get_connection(self):
        """
        Get database connection
        
        Returns:
            Database connection
        """
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(self.database_url)
        return self._connection
    
    def close_connection(self):
        """Close database connection"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None
    
    async def create_user(self, username: str, email: str, hashed_password: str, 
                         full_name: str, did: Optional[str] = None) -> Dict:
        """
        Create a new user
        
        Args:
            username: User's username
            email: User's email
            hashed_password: Hashed password
            full_name: User's full name
            did: Decentralized identifier (optional)
            
        Returns:
            User record
        """
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (username, email, hashed_password, full_name, did, wallet_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, username, email, full_name, did, wallet_id, is_active, created_at, updated_at
                    """,
                    (username, email, hashed_password, full_name, did, config.WALLET_NAME)
                )
                user = dict(cursor.fetchone())
                conn.commit()
                logger.info(f"User created: {username}")
                return user
        except psycopg2.IntegrityError as e:
            if conn:
                conn.rollback()
            logger.error(f"User creation failed (duplicate): {str(e)}")
            raise ValueError(f"Username or email already exists")
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"User creation failed: {str(e)}")
            raise
    
    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User record or None
        """
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, full_name, hashed_password, did, 
                           wallet_id, is_active, created_at, updated_at
                    FROM users
                    WHERE username = %s
                    """,
                    (username,)
                )
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get user by username: {str(e)}")
            raise
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User record or None
        """
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, full_name, hashed_password, did, 
                           wallet_id, is_active, created_at, updated_at
                    FROM users
                    WHERE id = %s
                    """,
                    (user_id,)
                )
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get user by ID: {str(e)}")
            raise
    
    async def update_user_did(self, user_id: int, did: str) -> bool:
        """
        Update user's DID
        
        Args:
            user_id: User ID
            did: Decentralized identifier
            
        Returns:
            True if successful
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET did = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (did, user_id)
                )
                conn.commit()
                logger.info(f"Updated DID for user {user_id}")
                return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update user DID: {str(e)}")
            raise
    
    async def update_user_email(self, user_id: int, email: str) -> bool:
        """
        Update user's email
        
        Args:
            user_id: User ID
            email: New email address
            
        Returns:
            True if successful
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET email = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (email, user_id)
                )
                conn.commit()
                logger.info(f"Updated email for user {user_id}")
                return True
        except psycopg2.IntegrityError:
            conn.rollback()
            raise ValueError("Email already exists")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update user email: {str(e)}")
            raise
    
    async def update_user_password(self, user_id: int, hashed_password: str) -> bool:
        """
        Update user's password
        
        Args:
            user_id: User ID
            hashed_password: New hashed password
            
        Returns:
            True if successful
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET hashed_password = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (hashed_password, user_id)
                )
                conn.commit()
                logger.info(f"Updated password for user {user_id}")
                return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update user password: {str(e)}")
            raise
    
    async def list_users(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        List all users
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List of user records
        """
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, full_name, did, wallet_id, 
                           is_active, created_at, updated_at
                    FROM users
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to list users: {str(e)}")
            raise
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                logger.info(f"Deleted user {user_id}")
                return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to delete user: {str(e)}")
            raise


# Global database service instance
db_service = DatabaseService()
