"""Image storage integration service using Supabase Storage."""

import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "sharebnb")
print(f"Supabase URL: {SUPABASE_URL}, Bucket: {SUPABASE_BUCKET}")
sb: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def upload_image(image_file, image_key):
    """Upload image to Supabase Storage.

    Args:
        image_file: Flask file object with image data
        image_key: Unique identifier for the image (used as path)

    Returns:
        bool: True if upload successful
    """
    sb.storage.from_(SUPABASE_BUCKET).upload(
        file=image_file,
        path=image_key,
        file_options={
            "content-type": image_file.content_type,
        }
    )

    return True


def generate_image_url(image_key):
    """Generate public URL for image in Supabase Storage.

    Args:
        image_key: Unique identifier for the image

    Returns:
        str: Public URL to access the image
    """
    response = sb.storage.from_(SUPABASE_BUCKET).get_public_url(image_key)
    return response
