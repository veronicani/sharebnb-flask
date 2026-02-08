"""Routes package for ShareBnB."""

from sharebnb.routes.properties import properties_bp


def register_routes(app):
    """Register all application routes."""
    app.register_blueprint(properties_bp)
