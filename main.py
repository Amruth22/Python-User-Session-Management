"""
User Session Management - Main Demonstration
Shows examples of all session and tracking features
"""

import os
import time
from session.session_manager import SessionManager
from tracking.activity_tracker import ActivityTracker
from tracking.event_logger import EventLogger
from tracking.behavioral_tracker import BehavioralTracker
from analytics.user_analytics import UserAnalytics
from analytics.analytics_reporter import AnalyticsReporter
from preferences.preference_manager import PreferenceManager
from compliance.gdpr_handler import GDPRHandler
from compliance.data_retention import DataRetentionPolicy
from compliance.privacy_manager import PrivacyManager


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_session_management():
    """Demonstrate session management"""
    print_section("1. Session Management")
    
    # Clean up old database
    db_path = 'demo.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    manager = SessionManager(db_path, session_timeout=3600)
    
    # Create session
    print("\n[EMOJI] Creating session for user 1...")
    session_id = manager.create_session(user_id=1, ip_address='192.168.1.100')
    print(f"   [EMOJI] Session created: {session_id[:20]}...")
    
    # Get session
    session = manager.get_session(session_id)
    print(f"   [EMOJI] Session retrieved: User {session['user_id']}")
    
    # Set session data
    manager.set_session_data(session_id, 'cart', {'items': ['Laptop'], 'total': 999.99})
    print("   [EMOJI] Session data stored")
    
    # Get session data
    cart = manager.get_session_data(session_id, 'cart')
    print(f"   [EMOJI] Session data retrieved: {cart}")
    
    # Get stats
    stats = manager.get_session_stats()
    print(f"\n[EMOJI] Session Stats:")
    print(f"   Active sessions: {stats['active_sessions']}")


def demo_activity_tracking():
    """Demonstrate activity tracking"""
    print_section("2. Activity Tracking")
    
    db_path = 'demo.db'
    tracker = ActivityTracker(db_path)
    event_logger = EventLogger(tracker)
    
    # Track events
    print("\n[EMOJI] Tracking user activities...")
    
    event_logger.log_login(user_id=1, session_id='session123', ip_address='192.168.1.100')
    print("   [EMOJI] Login tracked")
    
    event_logger.log_page_view(user_id=1, page='/dashboard', session_id='session123')
    print("   [EMOJI] Page view tracked")
    
    event_logger.log_action(user_id=1, action='button_click', details={'button': 'submit'}, session_id='session123')
    print("   [EMOJI] Action tracked")
    
    # Get activities
    activities = tracker.get_user_activities(user_id=1, limit=10)
    print(f"\n[EMOJI] User Activities: {len(activities)} events")
    
    for activity in activities[:3]:
        print(f"   - {activity['event_type']}")


def demo_user_analytics():
    """Demonstrate user analytics"""
    print_section("3. User Analytics")
    
    db_path = 'demo.db'
    analytics = UserAnalytics(db_path)
    
    # Get user summary
    print("\n[EMOJI] User Analytics Summary:")
    summary = analytics.get_user_summary(user_id=1)
    
    print(f"   Total Activities: {summary['total_activities']}")
    print(f"   Total Sessions: {summary['total_sessions']}")
    
    if summary['event_breakdown']:
        print(f"\n   Event Breakdown:")
        for event_type, count in summary['event_breakdown'].items():
            print(f"   - {event_type}: {count}")


def demo_behavioral_tracking():
    """Demonstrate behavioral tracking"""
    print_section("4. Behavioral Tracking")
    
    db_path = 'demo.db'
    tracker = BehavioralTracker(db_path)
    
    # Get user journey
    print("\n[EMOJI]️  User Journey:")
    journey = tracker.get_user_journey(user_id=1)
    
    print(f"   Total steps: {len(journey)}")
    for i, step in enumerate(journey[:5], 1):
        print(f"   {i}. {step['event_type']}")
    
    # Get common patterns
    print("\n[EMOJI] Common Patterns:")
    patterns = tracker.get_common_patterns(limit=5)
    
    for pattern in patterns:
        print(f"   - {pattern['event_type']}: {pattern['count']} times")


def demo_user_preferences():
    """Demonstrate user preferences"""
    print_section("5. User Preferences")
    
    db_path = 'demo.db'
    pref_manager = PreferenceManager(db_path)
    
    # Get default preferences
    print("\n[EMOJI]️  Default Preferences:")
    prefs = pref_manager.get_preferences(user_id=1)
    print(f"   Theme: {prefs['theme']}")
    print(f"   Language: {prefs['language']}")
    print(f"   Notifications: {prefs['notifications']}")
    
    # Update preference
    print("\n[EMOJI] Updating preferences...")
    pref_manager.update_preference(user_id=1, 'theme', 'dark')
    
    updated_prefs = pref_manager.get_preferences(user_id=1)
    print(f"   [EMOJI] Theme updated to: {updated_prefs['theme']}")


def demo_gdpr_compliance():
    """Demonstrate GDPR compliance"""
    print_section("6. GDPR Compliance")
    
    db_path = 'demo.db'
    gdpr = GDPRHandler(db_path)
    
    # Record consent
    print("\n[EMOJI] Recording user consent...")
    gdpr.record_consent(user_id=1, consent_type='analytics', granted=True)
    gdpr.record_consent(user_id=1, consent_type='marketing', granted=False)
    print("   [EMOJI] Consent recorded")
    
    # Get consent
    analytics_consent = gdpr.get_consent(user_id=1, 'analytics')
    print(f"   Analytics consent: {analytics_consent}")
    
    # Export user data
    print("\n[EMOJI] Exporting user data (Right to Access)...")
    export = gdpr.export_user_data(user_id=1)
    print(f"   [EMOJI] Data exported:")
    print(f"      Sessions: {len(export['sessions'])}")
    print(f"      Activities: {len(export['activities'])}")
    print(f"      Preferences: {len(export['preferences'])} settings")


def demo_data_retention():
    """Demonstrate data retention"""
    print_section("7. Data Retention Policy")
    
    db_path = 'demo.db'
    retention = DataRetentionPolicy(db_path, retention_days=90)
    
    print(f"\n[EMOJI]️  Data Retention Policy: {retention.retention_days} days")
    print("\n   Applying retention policy...")
    
    summary = retention.apply_retention_policy()
    
    print(f"   [EMOJI] Activities deleted: {summary['activities_deleted']}")
    print(f"   [EMOJI] Sessions deleted: {summary['sessions_deleted']}")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  User Session Management - Demonstration")
    print("=" * 70)
    
    try:
        demo_session_management()
        demo_activity_tracking()
        demo_user_analytics()
        demo_behavioral_tracking()
        demo_user_preferences()
        demo_gdpr_compliance()
        demo_data_retention()
        
        print("\n" + "=" * 70)
        print("  All Demonstrations Completed!")
        print("=" * 70)
        print("\nKey Features Demonstrated:")
        print("  1. Session Management - Create, validate, destroy")
        print("  2. Activity Tracking - Track user events")
        print("  3. User Analytics - Analyze behavior")
        print("  4. Behavioral Tracking - User journeys")
        print("  5. User Preferences - Settings management")
        print("  6. GDPR Compliance - Data rights")
        print("  7. Data Retention - Auto-cleanup")
        print("\nTo run Flask API:")
        print("  python api/app.py")
        print("\nTo run tests:")
        print("  python tests.py")
        print()
        
        # Cleanup
        if os.path.exists('demo.db'):
            os.remove('demo.db')
        
    except Exception as e:
        print(f"\n[EMOJI] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
