"""
Behavioral Tracker
Tracks user behavior patterns and journeys
"""

import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BehavioralTracker:
    """
    Tracks user behavior patterns
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize behavioral tracker
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Behavioral Tracker initialized")
    
    def get_user_journey(self, user_id, session_id=None):
        """
        Get user journey (sequence of events)
        
        Args:
            user_id: User ID
            session_id: Optional session ID filter
            
        Returns:
            List of events in order
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute('''
                SELECT event_type, event_data, timestamp 
                FROM activities 
                WHERE user_id = ? AND session_id = ? 
                ORDER BY timestamp ASC
            ''', (user_id, session_id))
        else:
            cursor.execute('''
                SELECT event_type, event_data, timestamp 
                FROM activities 
                WHERE user_id = ? 
                ORDER BY timestamp ASC 
                LIMIT 100
            ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        import json
        journey = []
        for row in rows:
            journey.append({
                'event_type': row['event_type'],
                'event_data': json.loads(row['event_data']) if row['event_data'] else {},
                'timestamp': row['timestamp']
            })
        
        return journey
    
    def get_common_patterns(self, limit=10):
        """
        Get common behavior patterns
        
        Args:
            limit: Number of patterns to return
            
        Returns:
            List of common patterns
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get most common event types
        cursor.execute('''
            SELECT event_type, COUNT(*) as count 
            FROM activities 
            GROUP BY event_type 
            ORDER BY count DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        patterns = []
        for row in rows:
            patterns.append({
                'event_type': row[0],
                'count': row[1]
            })
        
        return patterns
    
    def get_feature_usage(self, user_id):
        """
        Get feature usage statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Feature usage statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT event_type, COUNT(*) as count 
            FROM activities 
            WHERE user_id = ? 
            GROUP BY event_type
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        usage = {}
        for row in rows:
            usage[row[0]] = row[1]
        
        return usage
