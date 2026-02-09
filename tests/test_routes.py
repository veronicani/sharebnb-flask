"""Tests for ShareBnB routes."""

import pytest
import io
from unittest.mock import patch
from sharebnb.models import Property


class TestPropertyRoutes:
    """Tests for property routes."""

    def test_get_root(self, client):
        """Test GET / returns HTML."""
        response = client.get("/")

        assert response.status_code == 200
        assert b"html" in response.data.lower()

    def test_get_all_properties(self, client, db_session, sample_user):
        """Test GET /properties returns all properties."""
        # Create test properties
        prop1 = Property(
            name="Property 1",
            description="Description 1",
            address="123 Test St",
            price=100,
            backyard=True,
            pool=False,
            user_id=sample_user.id
        )
        prop2 = Property(
            name="Property 2",
            description="Description 2",
            address="456 Test Ave",
            price=200,
            backyard=False,
            pool=True,
            user_id=sample_user.id
        )
        db_session.add_all([prop1, prop2])
        db_session.commit()

        response = client.get("/properties")

        assert response.status_code == 200
        data = response.get_json()
        assert "properties" in data
        assert len(data["properties"]) == 2
        assert data["properties"][0]["name"] == "Property 1"
        assert data["properties"][1]["name"] == "Property 2"

    def test_get_properties_empty(self, client):
        """Test GET /properties returns empty list when no properties."""
        response = client.get("/properties")

        assert response.status_code == 200
        data = response.get_json()
        assert "properties" in data
        assert data["properties"] == []

    def test_get_properties_search_by_name(self, client, db_session, sample_user):
        """Test GET /properties?term=name filters by name."""
        prop1 = Property(
            name="Sunny Pool",
            description="Nice pool",
            address="123 Test St",
            price=100,
            backyard=True,
            pool=True,
            user_id=sample_user.id
        )
        prop2 = Property(
            name="Cozy Backyard",
            description="Nice backyard",
            address="456 Test Ave",
            price=150,
            backyard=True,
            pool=False,
            user_id=sample_user.id
        )
        db_session.add_all([prop1, prop2])
        db_session.commit()

        response = client.get("/properties?term=sunny")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["properties"]) == 1
        assert data["properties"][0]["name"] == "Sunny Pool"

    def test_get_properties_search_by_address(self, client, db_session, sample_user):
        """Test GET /properties?term=address filters by address."""
        prop1 = Property(
            name="Property 1",
            description="Description",
            address="123 Main Street",
            price=100,
            backyard=True,
            pool=False,
            user_id=sample_user.id
        )
        prop2 = Property(
            name="Property 2",
            description="Description",
            address="456 Elm Avenue",
            price=150,
            backyard=False,
            pool=True,
            user_id=sample_user.id
        )
        db_session.add_all([prop1, prop2])
        db_session.commit()

        response = client.get("/properties?term=main")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["properties"]) == 1
        assert data["properties"][0]["address"] == "123 Main Street"

    @patch('sharebnb.routes.properties.storage.upload_image')
    @patch('sharebnb.routes.properties.storage.generate_image_url')
    def test_post_property_success(self, mock_generate_url, mock_upload, client, db_session, sample_user):
        """Test POST /properties creates property and image."""
        mock_generate_url.return_value = "https://example.supabase.co/storage/v1/object/public/sharebnb-images/test-key"

        # Create mock file
        data = {
            'name': 'New Property',
            'description': 'A new property',
            'address': '789 New St',
            'price': '300',
            'backyard': 'true',
            'pool': 'false',
            'image': (io.BytesIO(b'mock image data'), 'test.jpg')
        }

        response = client.post(
            "/properties",
            data=data,
            content_type='multipart/form-data'
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "property" in data
        assert data["property"]["name"] == "New Property"
        assert data["property"]["price"] == 300
        assert data["property"]["backyard"] is True
        assert data["property"]["pool"] is False
        assert len(data["property"]["images"]) == 1

        # Verify image record was created
        assert mock_generate_url.called
        assert mock_upload.called

        # Verify property was added to database
        prop = db_session.query(Property).filter_by(name="New Property").first()
        assert prop is not None
        assert prop.description == "A new property"
        assert prop.address == "789 New St"
        assert prop.price == 300
        assert prop.backyard is True
        assert prop.pool is False

    def test_post_property_missing_field(self, client, db_session):
        """Test POST /properties with missing required field."""
        data = {
            'name': 'New Property',
            'description': 'A new property',
            # Missing address field
            'price': '300',
            'backyard': 'true',
            'pool': 'false'
        }

        response = client.post(
            "/properties",
            data=data,
            content_type='multipart/form-data'
        )

        assert response.status_code == 400
        assert "Missing required field" in response.get_json()['error']

    @patch('sharebnb.services.storage.upload_image')
    def test_add_property_upload_failure(self, mock_upload, client, db_session):
        """Test that a storage failure rolls back the database transaction."""
        
        mock_upload.return_value = False # Simulate Supabase failing

        data = {
            'name': 'Failure House',
            'description': 'Should not exist in DB',
            'address': '123 Fail Ln',
            'price': '100',
            'image': (io.BytesIO(b"data"), 'test.jpg')
        }

        response = client.post('/properties', data=data, content_type='multipart/form-data')

        assert response.status_code == 500
        
        prop = db_session.query(Property).filter_by(name="New Property").first()
        prop = Property.query.filter_by(name='Failure House').first()
        assert prop is None