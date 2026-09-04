"""
Zalia Security - Application Configuration
Centralized configuration management for all environments
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'localhost:3000,localhost:5000').split(',')
    
    # API Configuration
    API_TIMEOUT = 10
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB max request size
    JSON_SORT_KEYS = False
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_REQUESTS = 20
    RATELIMIT_WINDOW = 60  # seconds
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o-mini'
    OPENAI_TEMPERATURE = 0.8
    OPENAI_MAX_TOKENS = 500
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    RATELIMIT_REQUESTS = 10  # Stricter rate limiting in production
    RATELIMIT_WINDOW = 60


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    OPENAI_API_KEY = 'test-key'


# Configuration dictionary
config_by_env = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_env.get(env, DevelopmentConfig)
