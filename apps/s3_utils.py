import boto3


def upload_to_s3_and_get_url(file_obj, bucket_name, object_name):
    """
    파일을 S3에 업로드하고, 해당 객체의 영구 URL을 반환합니다.
    (이 URL에 접근하려면 해당 S3 객체는 Public Read 권한이 있어야 합니다)
    """
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_fileobj(
            file_obj,
            bucket_name,
            object_name,
            ExtraArgs={
                "ContentType": file_obj.content_type
            },  # ContentType을 명시해주는 것이 좋음
        )

        # 객체의 URL 구성 (리전에 따라 URL 형식이 다를 수 있음)
        # 예: https://<bucket-name>.s3.<region>.amazonaws.com/<object-name>
        url = f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{object_name}"
        return url

    except Exception as e:
        print(f"S3 Upload Failed: {e}")
        return None
