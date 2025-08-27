import boto3
from django.conf import settings
from uuid import uuid4

import mimetypes


def upload_to_s3(self, file, user):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    bucket = settings.AWS_STORAGE_BUCKET_NAME

    filename = f"products/{user.id}/{uuid4()}_{file.name}"

    # content_type 자동 추론 (없으면 기본값 image/jpeg)
    content_type = (
        file.content_type or mimetypes.guess_type(file.name)[0] or "image/jpeg"
    )

    s3.upload_fileobj(
        file,
        bucket,
        filename,
        ExtraArgs={"ACL": "public-read", "ContentType": content_type},
    )

    return f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
