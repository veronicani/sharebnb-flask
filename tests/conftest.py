"""Pytest configuration and fixtures for ShareBnB tests."""

import pytest
from sharebnb import create_app
from sharebnb.models import db, User, Property, Image


@pytest.fixture(scope="function")
def app():
    """Create application for testing."""
    from sqlalchemy import event

    app = create_app("testing")

    with app.app_context():
        # Enable foreign key constraints for SQLite
        @event.listens_for(db.engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Test client for making requests."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Database session for tests."""
    yield db.session


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for tests."""
    user = User(
        username="testuser",
        first_name="Test",
        last_name="User",
        email="test@test.com"
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_property(db_session, sample_user):
    """Create a sample property for tests."""
    prop = Property(
        name="Test Property",
        description="A test property",
        address="123 Test St",
        price=100,
        backyard=True,
        pool=False,
        user_id=sample_user.id
    )
    db_session.add(prop)
    db_session.commit()
    return prop


@pytest.fixture
def sample_image(db_session, sample_property):
    """Create a sample image for tests."""
    image = Image(
        property_id=sample_property.id,
        aws_key="test-key-123",
        url="https://bucket.s3.amazonaws.com/test-key-123"
    )
    db_session.add(image)
    db_session.commit()
    return image
