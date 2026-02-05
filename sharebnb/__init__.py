"""ShareBnB application factory."""

from flask import Flask
from flask_cors import CORS
from sharebnb.models.base import db


def create_app(config_name="development"):
    """Create and configure Flask application."""

    app = Flask(__name__, template_folder="../templates")
    CORS(app)

    config_map = {
        "development": "sharebnb.config.DevelopmentConfig",
        "testing": "sharebnb.config.TestingConfig",
        "production": "sharebnb.config.ProductionConfig",
    }
    app.config.from_object(config_map[config_name])

    db.init_app(app)

    from sharebnb.routes import register_routes
    register_routes(app)

    return app
