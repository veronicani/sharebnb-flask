"""Tests for ShareBnB models."""

import pytest
from sharebnb.models import User, Property, Image


class TestUserModel:
    """Tests for User model."""

    def test_user_creation(self, db_session):
        """Test creating a user."""
        user = User(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.email == "test@example.com"

    def test_user_serialize(self, db_session, sample_user):
        """Test user serialization."""
        serialized = sample_user.serialize()

        assert serialized["id"] == sample_user.id
        assert serialized["username"] == "testuser"
        assert serialized["first_name"] == "Test"
        assert serialized["last_name"] == "User"
        assert serialized["email"] == "test@test.com"

    def test_user_unique_username(self, db_session, sample_user):
        """Test that username must be unique."""
        duplicate_user = User(
            username="testuser",
            first_name="Another",
            last_name="User",
            email="another@test.com"
        )
        db_session.add(duplicate_user)

        with pytest.raises(Exception):
            db_session.commit()

    def test_user_cascade_delete(self, db_session, sample_user, sample_property):
        """Test that deleting user cascades to properties."""
        property_id = sample_property.id

        db_session.delete(sample_user)
        db_session.commit()

        deleted_property = db_session.query(Property).filter_by(id=property_id).first()
        assert deleted_property is None


class TestPropertyModel:
    """Tests for Property model."""

    def test_property_creation(self, db_session, sample_user):
        """Test creating a property."""
        prop = Property(
            name="Test House",
            description="A nice test house",
            address="123 Test Ave",
            price=150,
            backyard=True,
            pool=False,
            user_id=sample_user.id
        )
        db_session.add(prop)
        db_session.commit()

        assert prop.id is not None
        assert prop.name == "Test House"
        assert prop.description == "A nice test house"
        assert prop.address == "123 Test Ave"
        assert prop.price == 150
        assert prop.backyard is True
        assert prop.pool is False
        assert prop.user_id == sample_user.id

    def test_property_serialize(self, db_session, sample_property):
        """Test property serialization."""
        serialized = sample_property.serialize()

        assert serialized["id"] == sample_property.id
        assert serialized["name"] == "Test Property"
        assert serialized["description"] == "A test property"
        assert serialized["address"] == "123 Test St"
        assert serialized["price"] == 100
        assert serialized["backyard"] is True
        assert serialized["pool"] is False
        assert serialized["user_id"] == sample_property.user_id
        assert serialized["images"] == []


class TestImageModel:
    """Tests for Image model."""

    def test_image_creation(self, db_session, sample_property):
        """Test creating an image."""
        image = Image(
            property_id=sample_property.id,
            storage_key="test-key-456",
            url="https://bucket.s3.amazonaws.com/test-key-456"
        )
        db_session.add(image)
        db_session.commit()

        assert image.id is not None
        assert image.property_id == sample_property.id
        assert image.storage_key == "test-key-456"
        assert image.url == "https://bucket.s3.amazonaws.com/test-key-456"

    def test_image_serialize(self, db_session, sample_image):
        """Test image serialization."""
        serialized = sample_image.serialize()

        assert serialized["id"] == sample_image.id
        assert serialized["property_id"] == sample_image.property_id
        assert serialized["storage_key"] == "test-key-123"
        assert serialized["url"] == "https://bucket.s3.amazonaws.com/test-key-123"

    def test_image_cascade_delete(self, db_session, sample_property, sample_image):
        """Test that deleting property cascades to images."""
        image_id = sample_image.id

        db_session.delete(sample_property)
        db_session.commit()

        deleted_image = db_session.query(Image).filter_by(id=image_id).first()
        assert deleted_image is None
