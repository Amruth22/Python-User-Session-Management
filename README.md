# User Session Management

Educational Python application demonstrating **user session management**, **activity tracking**, **session state management**, **user activity analytics**, **behavioral tracking**, **user preferences**, and **compliance data handling** with **SQLite3 storage**.

## Features

### 🔐 Session Management
- **Session Creation** - Create secure sessions on login
- **Session Validation** - Verify session validity
- **Session Expiration** - Auto-expire old sessions
- **Session State** - Store arbitrary session data
- **Session Cleanup** - Remove expired sessions
- **Multi-Session Support** - Multiple sessions per user

### 📊 Activity Tracking
- **Event Tracking** - Track user actions and events
- **Event Types** - Login, logout, page views, actions
- **Event Logging** - Persistent event storage
- **Activity History** - Complete user activity log
- **Real-Time Tracking** - Track as events happen

### 📈 User Analytics
- **Activity Summary** - Total activities, sessions
- **Active Users** - Track active user count
- **Popular Pages** - Most visited pages
- **Session Duration** - Average session length
- **Event Breakdown** - Activities by type

### 🗺️ Behavioral Tracking
- **User Journey** - Track user flow through app
- **Common Patterns** - Identify behavior patterns
- **Feature Usage** - Track feature adoption
- **Conversion Funnel** - Track conversion steps

### ⚙️ User Preferences
- **Preference Storage** - Save user settings
- **Default Preferences** - Fallback values
- **Preference Categories** - Theme, language, notifications
- **Privacy Settings** - User privacy controls
- **Preference Updates** - Modify settings

### 🛡️ GDPR Compliance
- **Right to Access** - Export user data
- **Right to be Forgotten** - Delete user data
- **Consent Management** - Track user consent
- **Data Retention** - Auto-delete old data
- **Privacy Controls** - User privacy settings

### 💾 SQLite3 Storage
- **Persistent Storage** - Data survives restarts
- **Indexed Queries** - Fast data retrieval
- **Relational Data** - Proper data relationships
- **Transaction Support** - Data integrity

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Amruth22/Python-User-Session-Management.git
cd Python-User-Session-Management
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Demonstrations
```bash
python main.py
```

### 5. Run Flask API
```bash
python api/app.py
```

### 6. Run Tests
```bash
python tests.py
```

## Project Structure

```
Python-User-Session-Management/
│
├── session/
│   ├── session_manager.py       # Session management
│   ├── session_store.py         # SQLite session storage
│   └── session_middleware.py    # Flask middleware
│
├── tracking/
│   ├── activity_tracker.py      # Activity tracking
│   ├── event_logger.py          # Event logging
│   └── behavioral_tracker.py    # Behavior tracking
│
├── analytics/
│   ├── user_analytics.py        # User analytics
│   ├── activity_analytics.py    # Activity analysis
│   └── analytics_reporter.py    # Report generation
│
├── preferences/
│   ├── preference_manager.py    # Preference management
│   └── preference_store.py      # Preference storage
│
├── compliance/
│   ├── gdpr_handler.py          # GDPR compliance
│   ├── data_retention.py        # Data retention
│   └── privacy_manager.py       # Privacy management
│
├── api/
│   └── app.py                   # Flask API
│
├── main.py                      # Demonstration
├── tests.py                     # 10 unit tests
└── README.md                    # This file
```

## Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at REAL NOT NULL,
    expires_at REAL NOT NULL,
    last_activity REAL NOT NULL,
    data TEXT,
    ip_address TEXT,
    user_agent TEXT
)
```

### Activities Table
```sql
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id TEXT,
    event_type TEXT NOT NULL,
    event_data TEXT,
    ip_address TEXT,
    user_agent TEXT,
    timestamp REAL NOT NULL
)
```

### Preferences Table
```sql
CREATE TABLE preferences (
    user_id INTEGER PRIMARY KEY,
    preferences TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Consent Table
```sql
CREATE TABLE consent (
    user_id INTEGER,
    consent_type TEXT,
    granted BOOLEAN,
    timestamp REAL,
    PRIMARY KEY (user_id, consent_type)
)
```

## Usage Examples

### Session Management

```python
from session.session_manager import SessionManager

# Create session manager
manager = SessionManager('sessions.db', session_timeout=3600)

# Create session
session_id = manager.create_session(
    user_id=1,
    ip_address='192.168.1.100',
    user_agent='Mozilla/5.0...'
)

# Validate session
if manager.validate_session(session_id):
    print("Session is valid")

# Store data in session
manager.set_session_data(session_id, 'cart', {'items': [], 'total': 0})

# Get data from session
cart = manager.get_session_data(session_id, 'cart')

# Destroy session
manager.destroy_session(session_id)
```

### Activity Tracking

```python
from tracking.activity_tracker import ActivityTracker
from tracking.event_logger import EventLogger

# Create tracker
tracker = ActivityTracker('sessions.db')
event_logger = EventLogger(tracker)

# Track events
event_logger.log_login(user_id=1, session_id='session123')
event_logger.log_page_view(user_id=1, page='/dashboard')
event_logger.log_action(user_id=1, action='button_click', details={'button': 'submit'})

# Get user activities
activities = tracker.get_user_activities(user_id=1, limit=100)
```

### User Analytics

```python
from analytics.user_analytics import UserAnalytics

# Create analytics
analytics = UserAnalytics('sessions.db')

# Get user summary
summary = analytics.get_user_summary(user_id=1)
print(f"Total activities: {summary['total_activities']}")
print(f"Total sessions: {summary['total_sessions']}")

# Get active users
active_users = analytics.get_active_users(hours=24)
print(f"Active users (24h): {active_users}")

# Get popular pages
popular = analytics.get_popular_pages(limit=10)
```

### User Preferences

```python
from preferences.preference_manager import PreferenceManager

# Create manager
pref_manager = PreferenceManager('sessions.db')

# Get preferences
prefs = pref_manager.get_preferences(user_id=1)

# Update preference
pref_manager.update_preference(user_id=1, 'theme', 'dark')

# Set all preferences
pref_manager.set_preferences(user_id=1, {
    'theme': 'dark',
    'language': 'en',
    'notifications': {'email': True}
})
```

### GDPR Compliance

```python
from compliance.gdpr_handler import GDPRHandler

# Create handler
gdpr = GDPRHandler('sessions.db')

# Export user data (Right to Access)
export = gdpr.export_user_data(user_id=1)
# Returns all user data

# Delete user data (Right to be Forgotten)
summary = gdpr.delete_user_data(user_id=1)
# Deletes all user data

# Record consent
gdpr.record_consent(user_id=1, 'analytics', granted=True)

# Check consent
has_consent = gdpr.get_consent(user_id=1, 'analytics')
```

## API Endpoints

### Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

#### Logout
```http
POST /auth/logout
Cookie: session_id=<session_id>
```

### Session

#### Get Session Info
```http
GET /api/session
Cookie: session_id=<session_id>
```

### Activity Tracking

#### Track Page View
```http
POST /api/track/page
Cookie: session_id=<session_id>
Content-Type: application/json

{
  "page": "/dashboard"
}
```

#### Track Action
```http
POST /api/track/action
Cookie: session_id=<session_id>
Content-Type: application/json

{
  "action": "button_click",
  "details": {"button": "submit"}
}
```

### Analytics

#### Get User Analytics
```http
GET /api/analytics/user
Cookie: session_id=<session_id>
```

#### Get User Journey
```http
GET /api/analytics/journey
Cookie: session_id=<session_id>
```

### Preferences

#### Get Preferences
```http
GET /api/preferences
Cookie: session_id=<session_id>
```

#### Update Preferences
```http
PUT /api/preferences
Cookie: session_id=<session_id>
Content-Type: application/json

{
  "theme": "dark",
  "language": "en"
}
```

### GDPR

#### Export User Data
```http
GET /api/gdpr/export
Cookie: session_id=<session_id>
```

#### Delete User Data
```http
DELETE /api/gdpr/delete
Cookie: session_id=<session_id>
```

#### Record Consent
```http
POST /api/consent
Cookie: session_id=<session_id>
Content-Type: application/json

{
  "consent_type": "analytics",
  "granted": true
}
```

## Testing

Run the comprehensive test suite:

```bash
python tests.py
```

### Test Coverage (10 Tests)

1. ✅ **Session Creation** - Test session creation
2. ✅ **Session Expiration** - Test timeout
3. ✅ **Activity Tracking** - Test event tracking
4. ✅ **Session State** - Test data storage
5. ✅ **User Analytics** - Test analytics generation
6. ✅ **Behavioral Tracking** - Test user journey
7. ✅ **User Preferences** - Test preference management
8. ✅ **GDPR Export** - Test data export
9. ✅ **GDPR Deletion** - Test data deletion
10. ✅ **Data Retention** - Test auto-cleanup

## Educational Notes

### 1. Why Session Management?

**Benefits:**
- Track logged-in users
- Maintain user state
- Personalize experience
- Security and authentication

### 2. Activity Tracking

**Use Cases:**
- User behavior analysis
- Feature usage tracking
- Conversion optimization
- Debugging user issues

### 3. GDPR Compliance

**Requirements:**
- Right to access data
- Right to be forgotten
- Consent management
- Data portability

### 4. Data Retention

**Why Important:**
- Comply with regulations
- Manage storage costs
- Protect user privacy
- Reduce liability

## Production Considerations

For production use:

1. **Session Storage:**
   - Use Redis for sessions
   - Implement session clustering
   - Add session encryption

2. **Analytics:**
   - Use dedicated analytics DB
   - Implement data warehousing
   - Add real-time analytics

3. **Compliance:**
   - Implement full GDPR compliance
   - Add audit logging
   - Implement data encryption

4. **Performance:**
   - Index database properly
   - Use connection pooling
   - Implement caching

## Dependencies

- **Flask 3.0.0** - Web framework
- **python-dotenv 1.0.0** - Environment variables
- **pytest 7.4.3** - Testing framework
- **requests 2.31.0** - HTTP client
- **sqlite3** - Database (built-in)

## License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Learning! 🚀**
