"""This module contains the analysis repository"""

from datetime import timedelta
import logging
from os import getenv
import uuid
import boto3
from botocore.exceptions import ClientError

from analysis.models.analysis import Analysis
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import FileManagementRepository
from file_management.models.dataset import Dataset
from user_management.models.user import User


class FileManagementRepositoryImpl(FileManagementRepository):
    """Analysis repository"""

    def create_presigned_url_upload_file(self, filename: str, analysis_id: int):
        s3_client = boto3.client("s3")
        bucket_name = getenv("AWS_STORAGE_BUCKET_NAME")
        object_name = f"datasets/{analysis_id}/{filename}"
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

    def create_dataset(self, file_url: str, user_id: str, filename: str):
        """Create a new dataset"""
        user = User.objects.filter(id=user_id).first()

        new_dataset = Dataset.objects.create(
            url=file_url,
            filename=filename,
            uploaded_by=user
        )
        return DatasetTO.from_model(new_dataset)

    def attach_file_to_analysis(self, dataset_id: str, analysis_id: int) -> DatasetTO:
        analysis = Analysis.objects.filter(id=analysis_id).first()
        dataset = Dataset.objects.filter(id=dataset_id).first()
        analysis.datasets.add(dataset)
