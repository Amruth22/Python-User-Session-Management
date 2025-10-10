"""
Preference Manager
Manages user preferences with SQLite storage
"""

import sqlite3
import json
import logging

logger = logging.getLogger(__name__)


class PreferenceManager:
    """
    User preference manager with SQLite
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize preference manager
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        # Default preferences
        self.defaults = {
            'theme': 'light',
            'language': 'en',
            'notifications': {
                'email': True,
                'push': False,
                'sms': False
            },
            'privacy': {
                'profile_public': False,
                'show_activity': True,
                'allow_analytics': True
            }
        }
        
        logger.info("Preference Manager initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                user_id INTEGER PRIMARY KEY,
                preferences TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_preferences(self, user_id):
        """
        Get user preferences
        
        Args:
            user_id: User ID
            
        Returns:
            Preferences dictionary
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT preferences FROM preferences WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return json.loads(row['preferences'])
        else:
            # Return defaults
            return self.defaults.copy()
    
    def set_preferences(self, user_id, preferences):
        """
        Set user preferences
        
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
        
        logger.info(f"Preferences updated for user {user_id}")
    
    def update_preference(self, user_id, key, value):
        """
        Update a specific preference
        
        Args:
            user_id: User ID
            key: Preference key
            value: Preference value
        """
        preferences = self.get_preferences(user_id)
        preferences[key] = value
        self.set_preferences(user_id, preferences)
    
    def get_preference(self, user_id, key, default=None):
        """
        Get a specific preference
        
        Args:
            user_id: User ID
            key: Preference key
            default: Default value
            
        Returns:
            Preference value or default
        """
        preferences = self.get_preferences(user_id)
        return preferences.get(key, default)
    
    def reset_preferences(self, user_id):
        """
        Reset preferences to defaults
        
        Args:
            user_id: User ID
        """
        self.set_preferences(user_id, self.defaults.copy())
        logger.info(f"Preferences reset to defaults for user {user_id}")
