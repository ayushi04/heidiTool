import os

class Config:
    DEBUG = True
    TESTING = False
    PORT = 8080
    HOST = '0.0.0.0'
    BASE_DIR = os.getcwd()
    UPLOADS_DIR = os.path.join(BASE_DIR, 'static/uploads/')
    STATIC_DIR = os.path.join(BASE_DIR, 'static/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    DATABASE_CONNECT_OPTIONS = {}
    THREADS_PER_PAGE = 2
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = "secret"
    
class DevelopmentConfig(Config):
    DEBUG = True
    # Other development-specific configuration options...

class TestingConfig(Config):
    TESTING = True
    # Other testing-specific configuration options...
