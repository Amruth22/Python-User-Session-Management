"""
Privacy Manager
Manages user privacy settings and controls
"""

import logging

logger = logging.getLogger(__name__)


class PrivacyManager:
    """
    User privacy manager
    """
    
    def __init__(self, preference_manager):
        """
        Initialize privacy manager
        
        Args:
            preference_manager: PreferenceManager instance
        """
        self.preference_manager = preference_manager
        logger.info("Privacy Manager initialized")
    
    def set_profile_visibility(self, user_id, public):
        """
        Set profile visibility
        
        Args:
            user_id: User ID
            public: True for public, False for private
        """
        preferences = self.preference_manager.get_preferences(user_id)
        
        if 'privacy' not in preferences:
            preferences['privacy'] = {}
        
        preferences['privacy']['profile_public'] = public
        self.preference_manager.set_preferences(user_id, preferences)
        
        logger.info(f"Profile visibility set for user {user_id}: {'public' if public else 'private'}")
    
    def set_activity_visibility(self, user_id, visible):
        """
        Set activity visibility
        
        Args:
            user_id: User ID
            visible: True to show activity, False to hide
        """
        preferences = self.preference_manager.get_preferences(user_id)
        
        if 'privacy' not in preferences:
            preferences['privacy'] = {}
        
        preferences['privacy']['show_activity'] = visible
        self.preference_manager.set_preferences(user_id, preferences)
    
    def set_analytics_consent(self, user_id, allow):
        """
        Set analytics consent
        
        Args:
            user_id: User ID
            allow: True to allow analytics, False to opt out
        """
        preferences = self.preference_manager.get_preferences(user_id)
        
        if 'privacy' not in preferences:
            preferences['privacy'] = {}
        
        preferences['privacy']['allow_analytics'] = allow
        self.preference_manager.set_preferences(user_id, preferences)
        
        logger.info(f"Analytics consent for user {user_id}: {allow}")
    
    def get_privacy_settings(self, user_id):
        """
        Get all privacy settings
        
        Args:
            user_id: User ID
            
        Returns:
            Privacy settings dictionary
        """
        preferences = self.preference_manager.get_preferences(user_id)
        return preferences.get('privacy', {})
    
    def anonymize_ip(self, ip_address):
        """
        Anonymize IP address for privacy
        
        Args:
            ip_address: IP address
            
        Returns:
            Anonymized IP
        """
        if not ip_address:
            return None
        
        # Anonymize last octet for IPv4
        parts = ip_address.split('.')
        if len(parts) == 4:
            parts[-1] = '0'
            return '.'.join(parts)
        
        return ip_address
