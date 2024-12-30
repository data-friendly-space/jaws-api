"""This module contains the analysis repository"""

import logging
import urllib
from datetime import timedelta
from os import getenv
import boto3
from botocore.exceptions import ClientError
from django.db import transaction

from analysis.models.analysis import Analysis
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)
from file_management.models.dataset import Dataset
from user_management.models.user import User

bucket_name = getenv("AWS_STORAGE_BUCKET_NAME")


class FileManagementRepositoryImpl(FileManagementRepository):
    """Analysis repository"""

    def create_presigned_url_upload_file(self, filename: str, user_id: str):
        s3_client = boto3.client("s3")
        expires_in = timedelta(hours=1).seconds
        user = User.objects.filter(id=user_id).first()

        try:
            with transaction.atomic():
                new_dataset = Dataset.objects.create(
                    filename=filename, uploaded_by=user
                )
                object_name = f"datasets/{str(new_dataset.id)}"
                response = s3_client.generate_presigned_post(
                    bucket_name,
                    object_name,
                    ExpiresIn=expires_in,
                )

                new_dataset.url = f"{response['url']}{urllib.parse.quote(object_name)}"
                new_dataset.save()
        except ClientError as e:
            logging.error(e)
            raise e
        return S3PresignedUrlTO.from_model(response), DatasetTO.from_model(new_dataset)

    def create_presigned_url_download_file(self, dataset_id: str) -> str:
        s3_client = boto3.client("s3")
        object_name = f"datasets/{dataset_id}"
        expires_in = timedelta(hours=1).seconds
        try:
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logging.error(e)
            raise e
        return response

    def attach_file_to_analysis(self, dataset_id: str, analysis_id: int) -> DatasetTO:
        analysis = Analysis.objects.filter(id=analysis_id).first()
        dataset = Dataset.objects.filter(id=dataset_id).first()
        analysis.datasets.add(dataset)

    def get_dataset_by_id(self, dataset_id: str) -> DatasetTO:
        dataset = Dataset.objects.filter(id=dataset_id).first()
        return DatasetTO.from_model(dataset)
