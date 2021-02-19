from flask import Flask
from flask_mongoengine import MongoEngine
import os

db = MongoEngine()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.TestConfig')
    db.init_app(app)


    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        #app.register_blueprint(auth.auth_bp)
        #app.register_blueprint(admin.admin_bp)

        return app
