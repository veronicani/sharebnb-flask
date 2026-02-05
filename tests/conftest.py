"""Pytest configuration and fixtures for ShareBnB tests."""

import pytest
from sharebnb import create_app
from sharebnb.models import db, User, Property, Image


@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Test client for making requests."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Database session with automatic rollback."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        # Bind session to connection
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()


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
