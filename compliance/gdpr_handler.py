"""
GDPR Handler
Handles GDPR compliance requirements
"""

import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class GDPRHandler:
    """
    GDPR compliance handler
    Implements right to access, right to be forgotten, etc.
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize GDPR handler
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info("GDPR Handler initialized")
    
    def _init_database(self):
        """Initialize consent tracking table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consent (
                user_id INTEGER,
                consent_type TEXT,
                granted BOOLEAN,
                timestamp REAL,
                PRIMARY KEY (user_id, consent_type)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def export_user_data(self, user_id):
        """
        Export all user data (GDPR Right to Access)
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with all user data
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get sessions
        cursor.execute('SELECT * FROM sessions WHERE user_id = ?', (user_id,))
        sessions = [dict(row) for row in cursor.fetchall()]
        
        # Get activities
        cursor.execute('SELECT * FROM activities WHERE user_id = ?', (user_id,))
        activities = [dict(row) for row in cursor.fetchall()]
        
        # Get preferences
        cursor.execute('SELECT * FROM preferences WHERE user_id = ?', (user_id,))
        pref_row = cursor.fetchone()
        preferences = json.loads(pref_row['preferences']) if pref_row else {}
        
        # Get consent
        cursor.execute('SELECT * FROM consent WHERE user_id = ?', (user_id,))
        consent = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        export_data = {
            'user_id': user_id,
            'export_date': datetime.now().isoformat(),
            'sessions': sessions,
            'activities': activities,
            'preferences': preferences,
            'consent': consent
        }
        
        logger.info(f"User data exported for user {user_id}")
        
        return export_data
    
    def delete_user_data(self, user_id):
        """
        Delete all user data (GDPR Right to be Forgotten)
        
        Args:
            user_id: User ID
            
        Returns:
            Summary of deleted data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete sessions
        cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
        sessions_deleted = cursor.rowcount
        
        # Delete activities
        cursor.execute('DELETE FROM activities WHERE user_id = ?', (user_id,))
        activities_deleted = cursor.rowcount
        
        # Delete preferences
        cursor.execute('DELETE FROM preferences WHERE user_id = ?', (user_id,))
        preferences_deleted = cursor.rowcount
        
        # Delete consent
        cursor.execute('DELETE FROM consent WHERE user_id = ?', (user_id,))
        consent_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        summary = {
            'user_id': user_id,
            'sessions_deleted': sessions_deleted,
            'activities_deleted': activities_deleted,
            'preferences_deleted': preferences_deleted,
            'consent_deleted': consent_deleted,
            'deleted_at': datetime.now().isoformat()
        }
        
        logger.info(f"User data deleted for user {user_id}: {summary}")
        
        return summary
    
    def record_consent(self, user_id, consent_type, granted):
        """
        Record user consent
        
        Args:
            user_id: User ID
            consent_type: Type of consent (analytics, marketing, etc.)
            granted: Whether consent was granted
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().timestamp()
        
        cursor.execute('''
            INSERT OR REPLACE INTO consent (user_id, consent_type, granted, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, consent_type, granted, timestamp))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Consent recorded: user {user_id}, {consent_type} = {granted}")
    
    def get_consent(self, user_id, consent_type):
        """
        Get user consent status
        
        Args:
            user_id: User ID
            consent_type: Type of consent
            
        Returns:
            True if granted, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT granted FROM consent 
            WHERE user_id = ? AND consent_type = ?
        ''', (user_id, consent_type))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return bool(row['granted'])
        
        return False
    
    def get_all_consent(self, user_id):
        """
        Get all consent for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary of consent
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM consent WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        consent = {}
        for row in rows:
            consent[row['consent_type']] = bool(row['granted'])
        
        return consent
