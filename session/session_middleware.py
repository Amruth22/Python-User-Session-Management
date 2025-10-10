"""
Session Middleware
Flask middleware for session management
"""

import logging
from flask import request, g
from functools import wraps

logger = logging.getLogger(__name__)


class SessionMiddleware:
    """
    Session middleware for Flask
    """
    
    def __init__(self, app, session_manager):
        """
        Initialize session middleware
        
        Args:
            app: Flask app
            session_manager: SessionManager instance
        """
        self.app = app
        self.session_manager = session_manager
        
        # Register middleware
        self.app.before_request(self.before_request_handler)
        
        logger.info("Session Middleware initialized")
    
    def before_request_handler(self):
        """Handle session before each request"""
        # Get session ID from cookie or header
        session_id = request.cookies.get('session_id') or request.headers.get('X-Session-ID')
        
        if session_id:
            # Validate session
            session = self.session_manager.get_session(session_id)
            
            if session:
                # Store in g for access in routes
                g.session = session
                g.user_id = session['user_id']
                g.session_id = session_id
                
                logger.debug(f"Session validated: {session_id} for user {session['user_id']}")
            else:
                g.session = None
                g.user_id = None
                g.session_id = None
        else:
            g.session = None
            g.user_id = None
            g.session_id = None


def require_session(f):
    """
    Decorator to require valid session
    
    Usage:
        @app.route('/protected')
        @require_session
        def protected_route():
            return {'user_id': g.user_id}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'session') or g.session is None:
            from flask import jsonify
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Valid session required'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
