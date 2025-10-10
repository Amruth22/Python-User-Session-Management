"""
Session Manager
Manages user sessions with SQLite storage
"""

import secrets
import time
import logging
from datetime import datetime
from session.session_store import SessionStore

logger = logging.getLogger(__name__)


class SessionManager:
    """
    User session manager
    Handles session creation, validation, and cleanup
    """
    
    def __init__(self, db_path='sessions.db', session_timeout=3600):
        """
        Initialize session manager
        
        Args:
            db_path: Path to SQLite database
            session_timeout: Session timeout in seconds
        """
        self.store = SessionStore(db_path)
        self.session_timeout = session_timeout
        
        logger.info(f"Session Manager initialized (timeout: {session_timeout}s)")
    
    def create_session(self, user_id, ip_address=None, user_agent=None):
        """
        Create a new session
        
        Args:
            user_id: User ID
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Session ID
        """
        # Generate secure session ID
        session_id = secrets.token_urlsafe(32)
        
        # Calculate expiration
        expires_at = datetime.now().timestamp() + self.session_timeout
        
        # Create session in store
        self.store.create_session(session_id, user_id, expires_at, ip_address, user_agent)
        
        logger.info(f"Session created for user {user_id}: {session_id}")
        
        return session_id
    
    def get_session(self, session_id):
        """
        Get session by ID
        
        Args:
            session_id: Session ID
            
        Returns:
            Session dictionary or None
        """
        session = self.store.get_session(session_id)
        
        if not session:
            return None
        
        # Check if expired
        if self.is_expired(session):
            self.destroy_session(session_id)
            return None
        
        # Update last activity
        self.store.update_session_activity(session_id)
        
        return session
    
    def is_expired(self, session):
        """
        Check if session is expired
        
        Args:
            session: Session dictionary
            
        Returns:
            True if expired, False otherwise
        """
        current_time = datetime.now().timestamp()
        return current_time > session['expires_at']
    
    def validate_session(self, session_id):
        """
        Validate session
        
        Args:
            session_id: Session ID
            
        Returns:
            True if valid, False otherwise
        """
        session = self.get_session(session_id)
        return session is not None
    
    def destroy_session(self, session_id):
        """
        Destroy a session
        
        Args:
            session_id: Session ID
        """
        self.store.delete_session(session_id)
        logger.info(f"Session destroyed: {session_id}")
    
    def destroy_user_sessions(self, user_id):
        """
        Destroy all sessions for a user
        
        Args:
            user_id: User ID
        """
        self.store.delete_user_sessions(user_id)
        logger.info(f"All sessions destroyed for user {user_id}")
    
    def set_session_data(self, session_id, key, value):
        """
        Set data in session
        
        Args:
            session_id: Session ID
            key: Data key
            value: Data value
        """
        session = self.store.get_session(session_id)
        
        if session:
            session_data = session['data']
            session_data[key] = value
            self.store.set_session_data(session_id, session_data)
    
    def get_session_data(self, session_id, key, default=None):
        """
        Get data from session
        
        Args:
            session_id: Session ID
            key: Data key
            default: Default value if key not found
            
        Returns:
            Data value or default
        """
        session = self.store.get_session(session_id)
        
        if session:
            return session['data'].get(key, default)
        
        return default
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        deleted = self.store.delete_expired_sessions()
        logger.info(f"Cleaned up {deleted} expired sessions")
        return deleted
    
    def get_user_sessions(self, user_id):
        """
        Get all active sessions for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of sessions
        """
        return self.store.get_user_sessions(user_id)
    
    def get_session_stats(self):
        """Get session statistics"""
        active_count = self.store.get_active_sessions_count()
        
        return {
            'active_sessions': active_count,
            'session_timeout': self.session_timeout
        }
