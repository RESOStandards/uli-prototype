from application import create_app
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.yaml'  
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = environ.get('DEBUG')
    TESTING = environ.get('TESTING')
    MONGODB_DB = environ.get('MONGODB_DB')
    MONGODB_HOST = environ.get('MONGODB_HOST')
    MONGODB_USERNAME = environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD')

app = create_app(Config)

if __name__ == "__main__":
    app.run(host='0.0.0.0')