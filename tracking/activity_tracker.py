"""
Activity Tracker
Tracks user activities with SQLite storage
"""

import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ActivityTracker:
    """
    User activity tracker with SQLite
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize activity tracker
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info("Activity Tracker initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id TEXT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                ip_address TEXT,
                user_agent TEXT,
                timestamp REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_activities 
            ON activities(user_id, timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_event_type 
            ON activities(event_type)
        ''')
        
        conn.commit()
        conn.close()
    
    def track_event(self, user_id, event_type, event_data=None, session_id=None, 
                   ip_address=None, user_agent=None):
        """
        Track a user event
        
        Args:
            user_id: User ID
            event_type: Type of event (login, page_view, action, etc.)
            event_data: Additional event data
            session_id: Session ID
            ip_address: Client IP
            user_agent: Client user agent
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import json
        event_data_json = json.dumps(event_data) if event_data else None
        timestamp = datetime.now().timestamp()
        
        cursor.execute('''
            INSERT INTO activities (user_id, session_id, event_type, event_data, ip_address, user_agent, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, session_id, event_type, event_data_json, ip_address, user_agent, timestamp))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"Event tracked: {event_type} for user {user_id}")
    
    def get_user_activities(self, user_id, limit=100):
        """
        Get activities for a user
        
        Args:
            user_id: User ID
            limit: Maximum number of activities
            
        Returns:
            List of activities
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM activities 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        import json
        activities = []
        for row in rows:
            activities.append({
                'id': row['id'],
                'event_type': row['event_type'],
                'event_data': json.loads(row['event_data']) if row['event_data'] else {},
                'timestamp': row['timestamp'],
                'session_id': row['session_id']
            })
        
        return activities
    
    def get_activities_by_type(self, user_id, event_type):
        """
        Get activities by type for a user
        
        Args:
            user_id: User ID
            event_type: Event type to filter
            
        Returns:
            List of activities
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM activities 
            WHERE user_id = ? AND event_type = ? 
            ORDER BY timestamp DESC
        ''', (user_id, event_type))
        
        rows = cursor.fetchall()
        conn.close()
        
        import json
        activities = []
        for row in rows:
            activities.append({
                'id': row['id'],
                'event_type': row['event_type'],
                'event_data': json.loads(row['event_data']) if row['event_data'] else {},
                'timestamp': row['timestamp']
            })
        
        return activities
    
    def get_activity_count(self, user_id, event_type=None):
        """
        Get activity count for a user
        
        Args:
            user_id: User ID
            event_type: Optional event type filter
            
        Returns:
            Activity count
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if event_type:
            cursor.execute('''
                SELECT COUNT(*) FROM activities 
                WHERE user_id = ? AND event_type = ?
            ''', (user_id, event_type))
        else:
            cursor.execute('''
                SELECT COUNT(*) FROM activities 
                WHERE user_id = ?
            ''', (user_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def delete_old_activities(self, days=90):
        """
        Delete activities older than specified days
        
        Args:
            days: Number of days to retain
            
        Returns:
            Number of deleted activities
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        cursor.execute('DELETE FROM activities WHERE timestamp < ?', (cutoff_time,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} old activities (older than {days} days)")
        return deleted
