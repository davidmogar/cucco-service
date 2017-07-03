import os

class BaseConfig(object):
    """Parent configuration class."""
    CSRF_ENABLED = True
    DEBUG = False
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_ENABLED = False

class DevelopmentConfig(BaseConfig):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(BaseConfig):
    """Configurations for Testing.

    This Testing configuration uses a separate database.
    """
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
