"""
Analytics Reporter
Generates analytics reports
"""

import logging
from analytics.user_analytics import UserAnalytics
from analytics.activity_analytics import ActivityAnalytics

logger = logging.getLogger(__name__)


class AnalyticsReporter:
    """
    Generates analytics reports
    """
    
    def __init__(self, db_path='sessions.db'):
        """
        Initialize analytics reporter
        
        Args:
            db_path: Path to SQLite database
        """
        self.user_analytics = UserAnalytics(db_path)
        self.activity_analytics = ActivityAnalytics(db_path)
        
        logger.info("Analytics Reporter initialized")
    
    def generate_user_report(self, user_id):
        """
        Generate comprehensive user report
        
        Args:
            user_id: User ID
            
        Returns:
            User report dictionary
        """
        summary = self.user_analytics.get_user_summary(user_id)
        
        report = {
            'user_id': user_id,
            'summary': summary,
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def generate_system_report(self):
        """
        Generate system-wide analytics report
        
        Returns:
            System report dictionary
        """
        active_users_24h = self.user_analytics.get_active_users(hours=24)
        popular_pages = self.user_analytics.get_popular_pages(limit=5)
        top_users = self.activity_analytics.get_top_users(limit=5)
        hourly_activity = self.activity_analytics.get_activity_by_hour(hours=24)
        
        report = {
            'active_users_24h': active_users_24h,
            'popular_pages': popular_pages,
            'top_users': top_users,
            'hourly_activity': hourly_activity,
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def print_report(self, report):
        """
        Print analytics report
        
        Args:
            report: Report dictionary
        """
        print("\n" + "=" * 60)
        print("  ANALYTICS REPORT")
        print("=" * 60)
        
        if 'user_id' in report:
            # User report
            print(f"\nUser ID: {report['user_id']}")
            print(f"Total Activities: {report['summary']['total_activities']}")
            print(f"Total Sessions: {report['summary']['total_sessions']}")
        else:
            # System report
            print(f"\nActive Users (24h): {report['active_users_24h']}")
            print(f"\nTop Pages:")
            for page in report['popular_pages']:
                print(f"  - {page['page']}: {page['views']} views")
        
        print("\n" + "=" * 60)


from datetime import datetime
