"""Routes package for ShareBnB."""

from sharebnb.routes.properties import register_property_routes


def register_routes(app):
    """Register all application routes."""
    register_property_routes(app)
