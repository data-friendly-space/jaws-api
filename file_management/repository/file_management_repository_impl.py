"""This module contains the analysis repository"""

from datetime import timedelta
import logging
from os import getenv
import boto3
from botocore.exceptions import ClientError

from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO


class FileManagementRepositoryImpl:
    """Analysis repository"""

    def create_presigned_url_upload_file(self, filename: str):
        s3_client = boto3.client("s3")
        bucket_name = getenv("AWS_STORAGE_BUCKET_NAME")
        object_name = f"uploads/{filename}"
        expires_in = timedelta(hours=1).seconds

        try:
            response = s3_client.generate_presigned_post(
                bucket_name,
                object_name,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logging.error(e)
            raise e
        return S3PresignedUrlTO.from_model(response)
