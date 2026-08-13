import boto3

from config import Config


s3_client = boto3.client(
    "s3",
    region_name=Config.AWS_REGION,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
)


def upload_file(file_path, s3_key):
    s3_client.upload_file(
        str(file_path),
        Config.S3_BUCKET_NAME,
        s3_key,
    )

    return s3_key
