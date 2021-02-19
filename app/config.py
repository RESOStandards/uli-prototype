"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGODB_DB = environ.get('MONGODB_DB')
    MONGODB_HOST = environ.get('MONGODB_HOST')
    MONGODB_PORT = environ.get('MONGODB_PORT')
    MONGODB_USERNAME = environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD')

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGODB_DB = environ.get('MONGODB_DB')
    MONGODB_HOST = environ.get('MONGODB_HOST')
    MONGODB_PORT = environ.get('MONGODB_PORT')
    MONGODB_USERNAME = environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD')

class TestConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGO_DB = 'flaskdb'
    MONGODB_HOST = 'mongomock://localhost/'
