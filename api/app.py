"""
Flask API with Session Management
Demonstrates all session and tracking features
"""

from flask import Flask, request, jsonify, make_response, g
import logging
import os

from session.session_manager import SessionManager
from session.session_middleware import SessionMiddleware, require_session
from tracking.activity_tracker import ActivityTracker
from tracking.event_logger import EventLogger
from tracking.behavioral_tracker import BehavioralTracker
from analytics.user_analytics import UserAnalytics
from analytics.analytics_reporter import AnalyticsReporter
from preferences.preference_manager import PreferenceManager
from compliance.gdpr_handler import GDPRHandler
from compliance.data_retention import DataRetentionPolicy
from compliance.privacy_manager import PrivacyManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize components
db_path = os.getenv('DATABASE_PATH', 'sessions.db')
session_manager = SessionManager(db_path, session_timeout=3600)
activity_tracker = ActivityTracker(db_path)
event_logger = EventLogger(activity_tracker)
behavioral_tracker = BehavioralTracker(db_path)
user_analytics = UserAnalytics(db_path)
analytics_reporter = AnalyticsReporter(db_path)
preference_manager = PreferenceManager(db_path)
gdpr_handler = GDPRHandler(db_path)
data_retention = DataRetentionPolicy(db_path, retention_days=365)
privacy_manager = PrivacyManager(preference_manager)

# Add session middleware
session_middleware = SessionMiddleware(app, session_manager)

# Simple user database
users_db = {
    'admin': {'password': 'admin123', 'user_id': 1},
    'user1': {'password': 'user123', 'user_id': 2}
}


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'User Session Management API',
        'version': '1.0.0',
        'features': [
            'Session Management',
            'Activity Tracking',
            'User Analytics',
            'Behavioral Tracking',
            'User Preferences',
            'GDPR Compliance'
        ]
    })


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})


@app.route('/auth/login', methods=['POST'])
def login():
    """Login and create session"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    
    # Validate credentials
    if username in users_db and users_db[username]['password'] == password:
        user_id = users_db[username]['user_id']
        
        # Create session
        session_id = session_manager.create_session(
            user_id=user_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        # Track login event
        event_logger.log_login(user_id, session_id, request.remote_addr)
        
        # Create response with session cookie
        response = make_response(jsonify({
            'status': 'success',
            'message': 'Login successful',
            'session_id': session_id,
            'user_id': user_id
        }))
        
        response.set_cookie('session_id', session_id, httponly=True)
        
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/auth/logout', methods=['POST'])
@require_session
def logout():
    """Logout and destroy session"""
    session_id = g.session_id
    user_id = g.user_id
    
    # Track logout event
    event_logger.log_logout(user_id, session_id)
    
    # Destroy session
    session_manager.destroy_session(session_id)
    
    response = make_response(jsonify({
        'status': 'success',
        'message': 'Logout successful'
    }))
    
    response.set_cookie('session_id', '', expires=0)
    
    return response


@app.route('/api/session', methods=['GET'])
@require_session
def get_session_info():
    """Get current session information"""
    return jsonify({
        'session': g.session,
        'user_id': g.user_id
    })


@app.route('/api/track/page', methods=['POST'])
@require_session
def track_page_view():
    """Track page view"""
    data = request.get_json()
    
    if not data or 'page' not in data:
        return jsonify({'error': 'Page required'}), 400
    
    event_logger.log_page_view(g.user_id, data['page'], g.session_id)
    
    return jsonify({'status': 'success', 'message': 'Page view tracked'})


@app.route('/api/track/action', methods=['POST'])
@require_session
def track_action():
    """Track user action"""
    data = request.get_json()
    
    if not data or 'action' not in data:
        return jsonify({'error': 'Action required'}), 400
    
    event_logger.log_action(g.user_id, data['action'], data.get('details'), g.session_id)
    
    return jsonify({'status': 'success', 'message': 'Action tracked'})


@app.route('/api/analytics/user', methods=['GET'])
@require_session
def get_user_analytics():
    """Get user analytics"""
    summary = user_analytics.get_user_summary(g.user_id)
    
    return jsonify(summary)


@app.route('/api/analytics/journey', methods=['GET'])
@require_session
def get_user_journey():
    """Get user journey"""
    journey = behavioral_tracker.get_user_journey(g.user_id, g.session_id)
    
    return jsonify({
        'journey': journey,
        'steps': len(journey)
    })


@app.route('/api/preferences', methods=['GET'])
@require_session
def get_preferences():
    """Get user preferences"""
    preferences = preference_manager.get_preferences(g.user_id)
    
    return jsonify(preferences)


@app.route('/api/preferences', methods=['PUT'])
@require_session
def update_preferences():
    """Update user preferences"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Preferences data required'}), 400
    
    preference_manager.set_preferences(g.user_id, data)
    
    return jsonify({'status': 'success', 'message': 'Preferences updated'})


@app.route('/api/gdpr/export', methods=['GET'])
@require_session
def export_user_data():
    """Export user data (GDPR)"""
    export_data = gdpr_handler.export_user_data(g.user_id)
    
    return jsonify(export_data)


@app.route('/api/gdpr/delete', methods=['DELETE'])
@require_session
def delete_user_data():
    """Delete user data (GDPR)"""
    summary = gdpr_handler.delete_user_data(g.user_id)
    
    return jsonify(summary)


@app.route('/api/consent', methods=['POST'])
@require_session
def record_consent():
    """Record user consent"""
    data = request.get_json()
    
    if not data or 'consent_type' not in data or 'granted' not in data:
        return jsonify({'error': 'consent_type and granted required'}), 400
    
    gdpr_handler.record_consent(g.user_id, data['consent_type'], data['granted'])
    
    return jsonify({'status': 'success', 'message': 'Consent recorded'})


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print("User Session Management - Flask API")
    print("=" * 60)
    print(f"Starting on port {port}")
    print("Features enabled:")
    print("  - Session Management")
    print("  - Activity Tracking")
    print("  - User Analytics")
    print("  - User Preferences")
    print("  - GDPR Compliance")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
