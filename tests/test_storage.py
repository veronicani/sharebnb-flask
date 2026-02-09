"""Tests for Supabase storage service."""

import pytest
from unittest.mock import patch, MagicMock
from sharebnb.services import storage


class TestStorage:
    """Tests for Supabase storage integration."""

    @patch('storage.supabase.storage.from_')
    def test_upload_image__success(self, mock_supabase_from):
        """Test that upload_image calls Supabase with correct arguments."""

        # Mock the upload method to return a successful response
        mock_upload = mock_supabase_from.return_value.upload
        mock_upload.return_value = {"data": "success"}
        
        mock_file = MagicMock()
        mock_file.content_type = 'image/jpeg'
        image_key = 'test-image-123'

        result = storage.upload_image(mock_file, image_key)

        mock_supabase_from.assert_called_once_with(storage.SUPABASE_BUCKET)
        mock_supabase_from.storage.from_.return_value.upload.assert_called_once_with(
            file=mock_file,
            path=image_key,
            file_options={
                "content-type": 'image/jpeg'
            }
        )
        assert result is True

    @patch('storage.supabase')
    def test_generate_image_url__success(self, mock_supabase):
        """Test that generate_image_url calls Supabase with correct arguments."""
        from sharebnb.services.storage import generate_image_url

        image_key = 'test-image-123'
        expected_url = 'https://example.supabase.co/storage/v1/object/public/sharebnb-images/test-image-123'

        # Mock storage chain
        mock_storage = MagicMock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.get_public_url.return_value = expected_url

        # Call generate_image_url
        result = generate_image_url(image_key)

        # Verify supabase methods called with correct arguments
        mock_supabase.storage.from_.assert_called_once_with('sharebnb-images')
        mock_storage.get_public_url.assert_called_once_with(image_key)
        assert result == expected_url
