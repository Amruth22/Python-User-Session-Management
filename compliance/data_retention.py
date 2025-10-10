"""
Data Retention
Manages data retention policies
"""

import sqlite3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DataRetentionPolicy:
    """
    Data retention policy manager
    """
    
    def __init__(self, db_path='sessions.db', retention_days=365):
        """
        Initialize data retention policy
        
        Args:
            db_path: Path to SQLite database
            retention_days: Days to retain data
        """
        self.db_path = db_path
        self.retention_days = retention_days
        
        logger.info(f"Data Retention Policy initialized: {retention_days} days")
    
    def delete_old_activities(self):
        """
        Delete activities older than retention period
        
        Returns:
            Number of deleted activities
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now().timestamp() - (self.retention_days * 24 * 60 * 60)
        
        cursor.execute('DELETE FROM activities WHERE timestamp < ?', (cutoff_time,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} old activities")
        return deleted
    
    def delete_old_sessions(self):
        """
        Delete sessions older than retention period
        
        Returns:
            Number of deleted sessions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now().timestamp() - (self.retention_days * 24 * 60 * 60)
        
        cursor.execute('DELETE FROM sessions WHERE created_at < ?', (cutoff_time,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} old sessions")
        return deleted
    
    def apply_retention_policy(self):
        """
        Apply retention policy to all data
        
        Returns:
            Summary of deleted data
        """
        activities_deleted = self.delete_old_activities()
        sessions_deleted = self.delete_old_sessions()
        
        summary = {
            'activities_deleted': activities_deleted,
            'sessions_deleted': sessions_deleted,
            'retention_days': self.retention_days,
            'applied_at': datetime.now().isoformat()
        }
        
        logger.info(f"Retention policy applied: {summary}")
        
        return summary
