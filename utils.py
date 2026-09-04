"""
Zalia Security - Utility Functions
Common utilities for the application
"""

import re
from typing import Optional, Dict, Any
from datetime import datetime


def sanitize_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove excessive whitespace
    text = text.strip()
    
    # Limit length
    text = text[:max_length]
    
    # Remove potential HTML/Script injection
    text = re.sub(r'[<>]', '', text)
    
    return text


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate Nigerian phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Nigerian phone formats: +234..., 0..., etc.
    phone = re.sub(r'\D', '', phone)
    return len(phone) >= 10


def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
        fmt: Format string
        
    Returns:
        Formatted datetime string
    """
    if not isinstance(dt, datetime):
        return ""
    return dt.strftime(fmt)


def truncate_text(text: str, length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Text to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= length:
        return text
    return text[:length-len(suffix)] + suffix


def is_offline_request(request_method: str) -> bool:
    """
    Determine if request can be handled offline
    
    Args:
        request_method: HTTP method
        
    Returns:
        True if request type supports offline handling
    """
    return request_method in ['GET', 'HEAD', 'OPTIONS']


class ResponseFormatter:
    """Format API responses consistently"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        """
        Format successful response
        
        Args:
            data: Response data
            message: Success message
            
        Returns:
            Formatted response dict
        """
        return {
            "status": "success",
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str, code: str = "ERROR", details: Any = None) -> Dict[str, Any]:
        """
        Format error response
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            
        Returns:
            Formatted error dict
        """
        return {
            "status": "error",
            "message": message,
            "code": code,
            "details": details
        }
    
    @staticmethod
    def validation_error(field: str, message: str) -> Dict[str, Any]:
        """
        Format validation error
        
        Args:
            field: Field name
            message: Error message
            
        Returns:
            Formatted validation error dict
        """
        return {
            "status": "error",
            "type": "validation",
            "field": field,
            "message": message
        }


class LocationHelper:
    """Helper class for location-related operations"""
    
    PLACES = {
        'police': 'Police Stations',
        'hospital': 'Hospitals',
        'fire': 'Fire Stations',
        'pharmacy': 'Pharmacies',
        'petrol': 'Petrol Stations',
        'bank': 'Banks',
        'transport': 'Transport Services'
    }
    
    @staticmethod
    def get_emergency_places() -> Dict[str, str]:
        """Get emergency location types"""
        return LocationHelper.PLACES
    
    @staticmethod
    def get_place_emoji(place_type: str) -> str:
        """Get emoji for place type"""
        emojis = {
            'police': '🚔',
            'hospital': '🏥',
            'fire': '🚒',
            'pharmacy': '💊',
            'petrol': '⛽',
            'bank': '🏦',
            'transport': '🚕'
        }
        return emojis.get(place_type, '📍')


class SafetyTips:
    """Collection of safety tips and guidelines"""
    
    EMERGENCY_NUMBER = "112"
    
    TIPS = {
        'taxi': "Check vehicle before entering, share trip details, stay alert",
        'atm': "Cover PIN when entering, check surroundings, don't accept help",
        'night': "Use busy routes, inform someone where you're going",
        'phishing': "Don't click suspicious links, verify sender, never share PIN"
    }
    
    @staticmethod
    def get_tip(category: str) -> Optional[str]:
        """Get safety tip for category"""
        return SafetyTips.TIPS.get(category)
