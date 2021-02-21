from flask import Flask
from flask_mongoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint

db = MongoEngine()

def create_app(config):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)
    db.init_app(app)


    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        # Call factory function to create our blueprint
        swaggerui_blueprint = get_swaggerui_blueprint(
            config.SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
            config.API_URL,
            config={  # Swagger UI config overrides
                'app_name': "ULI Proof of Concept"
            },
        )

        app.register_blueprint(swaggerui_blueprint)

        #app.register_blueprint(auth.auth_bp)
        #app.register_blueprint(admin.admin_bp)

        return app
