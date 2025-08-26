"""
Configuration settings for Tummy Tracker application.
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tummy_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    
    # Machine Learning Configuration
    ML_MODEL_PATH = os.environ.get('ML_MODEL_PATH', 'data/models/')
    MIN_MEALS_FOR_ML = int(os.environ.get('MIN_MEALS_FOR_ML', '10'))
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'data/uploads/'
    
    # Pagination
    MEALS_PER_PAGE = 20
    SYMPTOMS_PER_PAGE = 20
    
    # Time Configuration
    SYMPTOM_TRACKING_WINDOW = 24  # hours after meal to track symptoms
    
    # Feature Flags
    ENABLE_ML_PREDICTIONS = True
    ENABLE_FOOD_IMAGES = False  # Future feature
    ENABLE_EXPORT_FEATURES = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tummy_tracker_dev.db'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tummy_tracker_test.db'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
