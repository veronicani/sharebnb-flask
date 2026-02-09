"""Tests for Supabase storage service."""

import pytest
from unittest.mock import patch, MagicMock
from sharebnb.services import storage


class TestStorage:
    """Tests for Supabase storage integration."""

    @patch('sharebnb.services.storage.sb.storage.from_')
    def test_upload_image__success(self, mock_supabase_from):
        """Test that upload_image calls Supabase with correct arguments."""

        # Mock the upload method to return a successful response
        mock_upload = mock_supabase_from.return_value.upload
        mock_upload.return_value = {"data": "success"}
        
        mock_file = MagicMock()
        mock_file.content_type = 'image/jpeg'
        image_key = 'test-image-123'

        result = storage.upload_image(mock_file, image_key)

        assert mock_supabase_from.call_count == 1
        assert mock_supabase_from.call_args[0][0] == storage.SUPABASE_BUCKET
        assert mock_supabase_from.return_value.upload.call_count == 1
        assert mock_supabase_from.return_value.upload.call_args[1] == dict(
            file=mock_file,
            path=image_key,
            file_options={
                "content-type": 'image/jpeg'
            }
        )
        assert result is True

    @patch('sharebnb.services.storage.sb.storage.from_')
    def test_generate_image_url__success(self, mock_supabase_from):
        """Test that generate_image_url calls Supabase with correct arguments."""

        image_key = 'test-image-123'

        mock_get_public_url = mock_supabase_from.return_value.get_public_url

        result = storage.generate_image_url(image_key)

        assert mock_supabase_from.call_count == 1
        assert mock_supabase_from.call_args[0][0] == storage.SUPABASE_BUCKET
        assert mock_get_public_url.call_count == 1
        assert mock_get_public_url.call_args[0][0] == image_key
