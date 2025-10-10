"""
Activity Analytics
Analyzes activity patterns and trends
"""

import sqlite3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ActivityAnalytics:
    """
    Activity analytics and reporting
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize activity analytics
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Activity Analytics initialized")
    
    def get_activity_by_hour(self, hours=24):
        """
        Get activity distribution by hour
        
        Args:
            hours: Number of hours to analyze
            
        Returns:
            Activity counts by hour
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        cursor.execute('''
            SELECT 
                strftime('%H', datetime(timestamp, 'unixepoch')) as hour,
                COUNT(*) as count
            FROM activities
            WHERE timestamp > ?
            GROUP BY hour
            ORDER BY hour
        ''', (cutoff_time,))
        
        rows = cursor.fetchall()
        conn.close()
        
        hourly_data = {}
        for row in rows:
            hourly_data[row[0]] = row[1]
        
        return hourly_data
    
    def get_top_users(self, limit=10):
        """
        Get most active users
        
        Args:
            limit: Number of users to return
            
        Returns:
            List of top users
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, COUNT(*) as activity_count
            FROM activities
            GROUP BY user_id
            ORDER BY activity_count DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        top_users = []
        for row in rows:
            top_users.append({
                'user_id': row[0],
                'activity_count': row[1]
            })
        
        return top_users
    
    def get_conversion_funnel(self, steps):
        """
        Get conversion funnel analytics
        
        Args:
            steps: List of event types representing funnel steps
            
        Returns:
            Funnel statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        funnel = []
        
        for step in steps:
            cursor.execute('''
                SELECT COUNT(DISTINCT user_id) 
                FROM activities 
                WHERE event_type = ?
            ''', (step,))
            
            count = cursor.fetchone()[0]
            funnel.append({
                'step': step,
                'users': count
            })
        
        conn.close()
        
        # Calculate conversion rates
        for i in range(1, len(funnel)):
            if funnel[i-1]['users'] > 0:
                conversion_rate = (funnel[i]['users'] / funnel[i-1]['users']) * 100
                funnel[i]['conversion_rate'] = f"{conversion_rate:.2f}%"
        
        return funnel
