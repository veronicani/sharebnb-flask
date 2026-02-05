"""AWS S3 integration service."""

import os
import boto3

AWS_BUCKET = os.environ.get('AWS_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION')

S3 = boto3.client(
    "s3",
    os.environ.get('AWS_REGION'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
)


def upload_image(image_file, aws_key):
    """Upload image to S3."""

    S3.upload_fileobj(
        image_file,
        AWS_BUCKET,
        aws_key,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": image_file.content_type
            }
    )

    return True


def generate_image_url(aws_key):
    """Generate S3 URL for image."""
    return f'https://{AWS_BUCKET}.s3.amazonaws.com/{aws_key}'
