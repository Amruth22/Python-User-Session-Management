"""
Session Store
SQLite-based session storage
"""

import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SessionStore:
    """
    SQLite-based session storage
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize session store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info(f"Session Store initialized with database: {db_path}")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                last_activity REAL NOT NULL,
                data TEXT,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Session database initialized")
    
    def create_session(self, session_id, user_id, expires_at, ip_address=None, user_agent=None):
        """
        Create a new session
        
        Args:
            session_id: Unique session ID
            user_id: User ID
            expires_at: Expiration timestamp
            ip_address: Client IP address
            user_agent: Client user agent
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().timestamp()
        
        cursor.execute('''
            INSERT INTO sessions (session_id, user_id, created_at, expires_at, last_activity, data, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, user_id, current_time, expires_at, current_time, '{}', ip_address, user_agent))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Session created: {session_id} for user {user_id}")
    
    def get_session(self, session_id):
        """
        Get session by ID
        
        Args:
            session_id: Session ID
            
        Returns:
            Session dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'session_id': row['session_id'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'expires_at': row['expires_at'],
                'last_activity': row['last_activity'],
                'data': json.loads(row['data']) if row['data'] else {},
                'ip_address': row['ip_address'],
                'user_agent': row['user_agent']
            }
        
        return None
    
    def update_session_activity(self, session_id):
        """
        Update last activity timestamp
        
        Args:
            session_id: Session ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().timestamp()
        
        cursor.execute('''
            UPDATE sessions SET last_activity = ? WHERE session_id = ?
        ''', (current_time, session_id))
        
        conn.commit()
        conn.close()
    
    def set_session_data(self, session_id, data):
        """
        Set session data
        
        Args:
            session_id: Session ID
            data: Data dictionary to store
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        data_json = json.dumps(data)
        
        cursor.execute('''
            UPDATE sessions SET data = ? WHERE session_id = ?
        ''', (data_json, session_id))
        
        conn.commit()
        conn.close()
    
    def delete_session(self, session_id):
        """
        Delete a session
        
        Args:
            session_id: Session ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Session deleted: {session_id}")
    
    def delete_user_sessions(self, user_id):
        """
        Delete all sessions for a user
        
        Args:
            user_id: User ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"All sessions deleted for user {user_id}")
    
    def delete_expired_sessions(self):
        """Delete all expired sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().timestamp()
        
        cursor.execute('DELETE FROM sessions WHERE expires_at < ?', (current_time,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} expired sessions")
        return deleted
    
    def get_user_sessions(self, user_id):
        """
        Get all sessions for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of sessions
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sessions WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append({
                'session_id': row['session_id'],
                'created_at': row['created_at'],
                'expires_at': row['expires_at'],
                'last_activity': row['last_activity']
            })
        
        return sessions
    
    def get_active_sessions_count(self):
        """Get count of active (non-expired) sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().timestamp()
        
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE expires_at > ?', (current_time,))
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count
