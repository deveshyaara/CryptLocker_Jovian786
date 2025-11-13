"""
Database Service
Handles PostgreSQL database operations for user management with connection pooling
"""

import logging
from datetime import datetime
from typing import Optional, Dict, List
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from config.agent_config import config

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations with connection pooling"""
    
    def __init__(self):
        """Initialize database service with connection pool"""
        self.database_url = config.DATABASE_URL
        # Create a thread-safe connection pool (min 1, max 10 connections)
        try:
            self._pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=self.database_url
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """
        Get database connection from pool using context manager
        Automatically handles commit/rollback and connection return
        
        Yields:
            Database connection
        """
        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self._pool.putconn(conn)
    
    def close_pool(self):
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            logger.info("Database connection pool closed")
    
    async def create_user(self, username: str, email: str, hashed_password: str, 
                         full_name: Optional[str] = None, did: Optional[str] = None) -> Dict:
        """
        Create a new user
        
        Args:
            username: User's username
            email: User's email
            hashed_password: Hashed password
            full_name: User's full name (optional)
            did: Decentralized identifier (optional)
            
        Returns:
            User record
        """
        try:
            with self.get_connection() as conn:
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
                    logger.info(f"User created: {username}")
                    return user
        except psycopg2.IntegrityError as e:
            logger.error(f"User creation failed (duplicate): {str(e)}")
            raise ValueError(f"Username or email already exists")
        except Exception as e:
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
            with self.get_connection() as conn:
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
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT id, username, email, full_name, did, wallet_id, 
                               is_active, created_at, updated_at
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
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE users
                        SET did = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (did, user_id)
                    )
                    logger.info(f"Updated DID for user {user_id}")
                    return True
        except Exception as e:
            logger.error(f"Failed to update user DID: {str(e)}")
            raise
    
    async def update_user_email(self, user_id: int, email: str) -> bool:
        """
        Update user's email
        
        Args:
            user_id: User ID
            email: Email address
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE users
                        SET email = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (email, user_id)
                    )
                    logger.info(f"Updated email for user {user_id}")
                    return True
        except psycopg2.IntegrityError as e:
            logger.error(f"Email update failed (duplicate): {str(e)}")
            raise ValueError("Email already exists")
        except Exception as e:
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
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE users
                        SET hashed_password = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (hashed_password, user_id)
                    )
                    logger.info(f"Updated password for user {user_id}")
                    return True
        except Exception as e:
            logger.error(f"Failed to update user password: {str(e)}")
            raise
    
    async def list_users(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        List users
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List of user records
        """
        try:
            with self.get_connection() as conn:
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
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
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
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM users WHERE id = %s
                        """,
                        (user_id,)
                    )
                    logger.info(f"Deleted user {user_id}")
                    return True
        except Exception as e:
            logger.error(f"Failed to delete user: {str(e)}")
            raise


# Lazy singleton instance - initialized on first use
_db_service_instance = None


def get_db_service():
    """Get or create the database service singleton"""
    global _db_service_instance
    if _db_service_instance is None:
        _db_service_instance = DatabaseService()
    return _db_service_instance


# For backward compatibility
db_service = get_db_service()
