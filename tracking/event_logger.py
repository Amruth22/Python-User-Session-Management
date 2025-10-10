"""
Event Logger
Logs user events for tracking
"""

import logging

logger = logging.getLogger(__name__)


class EventLogger:
    """
    Event logging system
    """
    
    # Event types
    EVENT_LOGIN = 'login'
    EVENT_LOGOUT = 'logout'
    EVENT_PAGE_VIEW = 'page_view'
    EVENT_BUTTON_CLICK = 'button_click'
    EVENT_FORM_SUBMIT = 'form_submit'
    EVENT_API_CALL = 'api_call'
    EVENT_ERROR = 'error'
    EVENT_PURCHASE = 'purchase'
    
    def __init__(self, activity_tracker):
        """
        Initialize event logger
        
        Args:
            activity_tracker: ActivityTracker instance
        """
        self.tracker = activity_tracker
        logger.info("Event Logger initialized")
    
    def log_login(self, user_id, session_id, ip_address=None):
        """Log login event"""
        self.tracker.track_event(
            user_id=user_id,
            event_type=self.EVENT_LOGIN,
            event_data={'action': 'user_logged_in'},
            session_id=session_id,
            ip_address=ip_address
        )
    
    def log_logout(self, user_id, session_id):
        """Log logout event"""
        self.tracker.track_event(
            user_id=user_id,
            event_type=self.EVENT_LOGOUT,
            event_data={'action': 'user_logged_out'},
            session_id=session_id
        )
    
    def log_page_view(self, user_id, page, session_id=None):
        """Log page view event"""
        self.tracker.track_event(
            user_id=user_id,
            event_type=self.EVENT_PAGE_VIEW,
            event_data={'page': page},
            session_id=session_id
        )
    
    def log_action(self, user_id, action, details=None, session_id=None):
        """Log user action"""
        self.tracker.track_event(
            user_id=user_id,
            event_type=self.EVENT_BUTTON_CLICK,
            event_data={'action': action, 'details': details},
            session_id=session_id
        )
    
    def log_api_call(self, user_id, endpoint, method, session_id=None):
        """Log API call"""
        self.tracker.track_event(
            user_id=user_id,
            event_type=self.EVENT_API_CALL,
            event_data={'endpoint': endpoint, 'method': method},
            session_id=session_id
        )
