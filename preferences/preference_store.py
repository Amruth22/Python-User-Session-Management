"""
Preference Store
Low-level preference storage operations
"""

import sqlite3
import json
import logging

logger = logging.getLogger(__name__)


class PreferenceStore:
    """
    Low-level preference storage
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize preference store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Preference Store initialized")
    
    def save(self, user_id, preferences):
        """
        Save preferences
        
        Args:
            user_id: User ID
            preferences: Preferences dictionary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        preferences_json = json.dumps(preferences)
        
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (user_id, preferences, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, preferences_json))
        
        conn.commit()
        conn.close()
    
    def load(self, user_id):
        """
        Load preferences
        
        Args:
            user_id: User ID
            
        Returns:
            Preferences dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT preferences FROM preferences WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return json.loads(row['preferences'])
        
        return None
    
    def delete(self, user_id):
        """
        Delete preferences
        
        Args:
            user_id: User ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM preferences WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Preferences deleted for user {user_id}")
