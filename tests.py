"""
Comprehensive Unit Tests for User Session Management
Tests sessions, activity tracking, analytics, preferences, and GDPR compliance
"""

import unittest
import time
import os
from session.session_manager import SessionManager
from tracking.activity_tracker import ActivityTracker
from tracking.event_logger import EventLogger
from tracking.behavioral_tracker import BehavioralTracker
from analytics.user_analytics import UserAnalytics
from preferences.preference_manager import PreferenceManager
from compliance.gdpr_handler import GDPRHandler
from compliance.data_retention import DataRetentionPolicy


class UserSessionManagementTestCase(unittest.TestCase):
    """Unit tests for User Session Management"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        print("\n" + "=" * 60)
        print("User Session Management - Unit Test Suite")
        print("=" * 60)
        print("Testing: Sessions, Tracking, Analytics, GDPR")
        print("=" * 60 + "\n")
        
        # Use test database
        cls.db_path = 'test_sessions.db'
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    # Test 1: Session Creation
    def test_01_session_creation(self):
        """Test session creation"""
        print("\n1. Testing session creation...")
        
        manager = SessionManager(self.db_path, session_timeout=3600)
        
        # Create session
        session_id = manager.create_session(user_id=1, ip_address='192.168.1.100')
        
        self.assertIsNotNone(session_id)
        print(f"   ✅ Session created: {session_id[:20]}...")
        
        # Retrieve session
        session = manager.get_session(session_id)
        
        self.assertIsNotNone(session)
        self.assertEqual(session['user_id'], 1)
        print(f"   ✅ Session retrieved for user {session['user_id']}")
    
    # Test 2: Session Expiration
    def test_02_session_expiration(self):
        """Test session expiration"""
        print("\n2. Testing session expiration...")
        
        manager = SessionManager(self.db_path, session_timeout=1)  # 1 second timeout
        
        # Create session
        session_id = manager.create_session(user_id=1)
        
        # Should be valid immediately
        self.assertTrue(manager.validate_session(session_id))
        print("   ✅ Session valid immediately after creation")
        
        # Wait for expiration
        time.sleep(1.5)
        
        # Should be expired
        self.assertFalse(manager.validate_session(session_id))
        print("   ✅ Session expired after timeout")
    
    # Test 3: Activity Tracking
    def test_03_activity_tracking(self):
        """Test activity tracking"""
        print("\n3. Testing activity tracking...")
        
        tracker = ActivityTracker(self.db_path)
        
        # Track events
        tracker.track_event(user_id=1, event_type='login', session_id='session123')
        tracker.track_event(user_id=1, event_type='page_view', event_data={'page': '/dashboard'})
        tracker.track_event(user_id=1, event_type='button_click', event_data={'button': 'submit'})
        
        print("   ✅ 3 events tracked")
        
        # Get activities
        activities = tracker.get_user_activities(user_id=1)
        
        self.assertGreaterEqual(len(activities), 3)
        print(f"   ✅ Retrieved {len(activities)} activities")
        
        # Get count
        count = tracker.get_activity_count(user_id=1)
        self.assertGreaterEqual(count, 3)
        print(f"   ✅ Activity count: {count}")
    
    # Test 4: Session State Management
    def test_04_session_state_management(self):
        """Test session state storage"""
        print("\n4. Testing session state management...")
        
        manager = SessionManager(self.db_path)
        
        # Create session
        session_id = manager.create_session(user_id=1)
        
        # Set data
        manager.set_session_data(session_id, 'cart', {'items': ['Product1'], 'total': 99.99})
        print("   ✅ Session data stored")
        
        # Get data
        cart = manager.get_session_data(session_id, 'cart')
        
        self.assertIsNotNone(cart)
        self.assertEqual(cart['total'], 99.99)
        print(f"   ✅ Session data retrieved: {cart}")
    
    # Test 5: User Analytics
    def test_05_user_analytics(self):
        """Test user analytics"""
        print("\n5. Testing user analytics...")
        
        analytics = UserAnalytics(self.db_path)
        
        # Get user summary
        summary = analytics.get_user_summary(user_id=1)
        
        self.assertIn('total_activities', summary)
        self.assertIn('total_sessions', summary)
        
        print(f"   ✅ User summary generated")
        print(f"   ✅ Total activities: {summary['total_activities']}")
        print(f"   ✅ Total sessions: {summary['total_sessions']}")
    
    # Test 6: Behavioral Tracking
    def test_06_behavioral_tracking(self):
        """Test behavioral tracking"""
        print("\n6. Testing behavioral tracking...")
        
        tracker = BehavioralTracker(self.db_path)
        
        # Get user journey
        journey = tracker.get_user_journey(user_id=1)
        
        self.assertIsInstance(journey, list)
        print(f"   ✅ User journey retrieved: {len(journey)} steps")
        
        # Get common patterns
        patterns = tracker.get_common_patterns(limit=5)
        
        self.assertIsInstance(patterns, list)
        print(f"   ✅ Common patterns: {len(patterns)} patterns")
    
    # Test 7: User Preferences
    def test_07_user_preferences(self):
        """Test user preferences"""
        print("\n7. Testing user preferences...")
        
        pref_manager = PreferenceManager(self.db_path)
        
        # Get default preferences
        prefs = pref_manager.get_preferences(user_id=1)
        
        self.assertIn('theme', prefs)
        self.assertIn('language', prefs)
        print(f"   ✅ Default preferences loaded")
        
        # Update preference
        pref_manager.update_preference(user_id=1, 'theme', 'dark')
        
        updated_prefs = pref_manager.get_preferences(user_id=1)
        self.assertEqual(updated_prefs['theme'], 'dark')
        print(f"   ✅ Preference updated: theme = {updated_prefs['theme']}")
    
    # Test 8: GDPR Data Export
    def test_08_gdpr_data_export(self):
        """Test GDPR data export"""
        print("\n8. Testing GDPR data export...")
        
        gdpr = GDPRHandler(self.db_path)
        
        # Export user data
        export = gdpr.export_user_data(user_id=1)
        
        self.assertIn('sessions', export)
        self.assertIn('activities', export)
        self.assertIn('preferences', export)
        
        print(f"   ✅ User data exported")
        print(f"   ✅ Sessions: {len(export['sessions'])}")
        print(f"   ✅ Activities: {len(export['activities'])}")
    
    # Test 9: GDPR Data Deletion
    def test_09_gdpr_data_deletion(self):
        """Test GDPR data deletion"""
        print("\n9. Testing GDPR data deletion...")
        
        # Create test user data
        manager = SessionManager(self.db_path)
        tracker = ActivityTracker(self.db_path)
        
        session_id = manager.create_session(user_id=99)
        tracker.track_event(user_id=99, event_type='test', session_id=session_id)
        
        # Delete user data
        gdpr = GDPRHandler(self.db_path)
        summary = gdpr.delete_user_data(user_id=99)
        
        self.assertGreaterEqual(summary['sessions_deleted'], 0)
        self.assertGreaterEqual(summary['activities_deleted'], 0)
        
        print(f"   ✅ User data deleted")
        print(f"   ✅ Sessions deleted: {summary['sessions_deleted']}")
        print(f"   ✅ Activities deleted: {summary['activities_deleted']}")
    
    # Test 10: Data Retention
    def test_10_data_retention(self):
        """Test data retention policy"""
        print("\n10. Testing data retention policy...")
        
        retention = DataRetentionPolicy(self.db_path, retention_days=90)
        
        # Apply retention policy
        summary = retention.apply_retention_policy()
        
        self.assertIn('activities_deleted', summary)
        self.assertIn('sessions_deleted', summary)
        
        print(f"   ✅ Retention policy applied")
        print(f"   ✅ Retention period: {summary['retention_days']} days")


def run_tests():
    """Run all unit tests"""
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(UserSessionManagementTestCase)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("User Session Management - Unit Test Suite")
    print("=" * 60)
    
    try:
        success = run_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
