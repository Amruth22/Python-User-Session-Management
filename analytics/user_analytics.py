"""
User Analytics
Analyzes user activity and behavior with SQLite
"""

import sqlite3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class UserAnalytics:
    """
    User activity analytics with SQLite
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize user analytics
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("User Analytics initialized")
    
    def get_user_summary(self, user_id):
        """
        Get summary of user activity
        
        Args:
            user_id: User ID
            
        Returns:
            User activity summary
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total activities
        cursor.execute('SELECT COUNT(*) FROM activities WHERE user_id = ?', (user_id,))
        total_activities = cursor.fetchone()[0]
        
        # Total sessions
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE user_id = ?', (user_id,))
        total_sessions = cursor.fetchone()[0]
        
        # Most recent activity
        cursor.execute('''
            SELECT timestamp FROM activities 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (user_id,))
        
        last_activity_row = cursor.fetchone()
        last_activity = last_activity_row[0] if last_activity_row else None
        
        # Event type breakdown
        cursor.execute('''
            SELECT event_type, COUNT(*) as count 
            FROM activities 
            WHERE user_id = ? 
            GROUP BY event_type
        ''', (user_id,))
        
        event_breakdown = {}
        for row in cursor.fetchall():
            event_breakdown[row[0]] = row[1]
        
        conn.close()
        
        return {
            'user_id': user_id,
            'total_activities': total_activities,
            'total_sessions': total_sessions,
            'last_activity': last_activity,
            'event_breakdown': event_breakdown
        }
    
    def get_active_users(self, hours=24):
        """
        Get count of active users in last N hours
        
        Args:
            hours: Time window in hours
            
        Returns:
            Count of active users
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) 
            FROM activities 
            WHERE timestamp > ?
        ''', (cutoff_time,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_popular_pages(self, limit=10):
        """
        Get most popular pages
        
        Args:
            limit: Number of pages to return
            
        Returns:
            List of popular pages
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT event_data, COUNT(*) as count 
            FROM activities 
            WHERE event_type = 'page_view' 
            GROUP BY event_data 
            ORDER BY count DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        import json
        pages = []
        for row in rows:
            try:
                data = json.loads(row[0]) if row[0] else {}
                pages.append({
                    'page': data.get('page', 'unknown'),
                    'views': row[1]
                })
            except:
                pass
        
        return pages
    
    def get_session_duration_avg(self, user_id=None):
        """
        Get average session duration
        
        Args:
            user_id: Optional user ID filter
            
        Returns:
            Average duration in seconds
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT created_at, last_activity 
                FROM sessions 
                WHERE user_id = ?
            ''', (user_id,))
        else:
            cursor.execute('SELECT created_at, last_activity FROM sessions')
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return 0
        
        durations = [row[1] - row[0] for row in rows if row[1] and row[0]]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return avg_duration
