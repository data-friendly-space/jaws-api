"""This module contains the analysis repository"""

import logging
import urllib
from datetime import timedelta
from os import getenv
from typing import List
from django.db import transaction

import boto3
import boto3.exceptions
import boto3.s3
from botocore.exceptions import ClientError

from analysis.models.analysis import Analysis
from common.helpers.get_mime_type_from_extension import get_mimetype_from_extension
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_object_attributes_to import S3ObjectAttributesTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset
from user_management.models.user import User

bucket_name = getenv("AWS_STORAGE_BUCKET_NAME")


class FileManagementRepositoryImpl(FileManagementRepository):
    """Analysis repository"""

    def create_presigned_url_upload_file(self, filename: str):
        s3_client = boto3.client("s3")
        expires_in = timedelta(hours=1).seconds
        try:
            object_name = f"datasets/{filename}"
            response = s3_client.generate_presigned_post(
                bucket_name,
                object_name,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logging.error(e)
            raise e
        return S3PresignedUrlTO.from_model(response)

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

    def get_dataset_by_id(self, dataset_id: str) -> DatasetTO | None:
        dataset = Dataset.objects.filter(id=dataset_id).first()
        return DatasetTO.from_model(dataset)

    def get_analysis_datasets(self, analysis_id: int) -> List[DatasetTO]:
        analysis = Analysis.objects.filter(id=analysis_id).first()
        datasets = analysis.datasets.all()
        return DatasetTO.from_models(datasets)

    def get_dataset_by_filename(self, filename):
        dataset = Dataset.objects.filter(filename=filename).first()
        return dataset

    def get_dataset_file(self, filename):
        s3_client = boto3.client("s3")
        try:
            s3_object = s3_client.get_object(
                Bucket=bucket_name,
                Key=f"datasets/{filename}"
            )
        except ClientError as e:
            logging.error(e)
            raise e
        return S3ObjectAttributesTO.from_model(s3_object)

    def create_dataset(
            self,
            filename: str,
            size_bytes: int,
            user_id: str,
            total_rows: int,
            total_columns: int):
        user = User.objects.get(id=user_id)
        new_dataset, _ = Dataset.objects.update_or_create(
            filename=filename,
            size_bytes=size_bytes,
            uploaded_by=user,
            mime_type=get_mimetype_from_extension(filename),
            url=f"https://{bucket_name}.s3.amazonaws.com/datasets/{urllib.parse.quote(filename)}",
            total_rows=total_rows,
            total_columns=total_columns
        )
        return DatasetTO.from_model(new_dataset)

    def create_columns(self, dataset_id, columns: List[str]) -> List[ColumnConfigurationTO]:
        dataset = Dataset.objects.get(id=dataset_id)
        column_configurations = []
        for col in columns:
            new_column_config, _ = ColumnConfiguration.objects.update_or_create(
                    dataset=dataset,
                    original_name=col
                )
            column_configurations.append(
                new_column_config
            )
        return ColumnConfigurationTO.from_models(column_configurations)

    def get_dataset_columns(self, dataset_id):
        column_configurations = ColumnConfiguration.objects.filter(
            dataset__id=dataset_id
        ).all()
        return ColumnConfigurationTO.from_models(column_configurations)

    @transaction.atomic
    def update_columns(self, columns):
        for column in columns.data:
            column_configuration = ColumnConfiguration.objects.get(id=column["id"])
            column_configuration.alias = column["alias"]
            column_configuration.include = column["include"]
            column_configuration.save()

    def update_dataset(self, analysis_id, filename, csv):
        s3 = boto3.client("s3")
        try:
            response = s3.put_object(
                Bucket=bucket_name,
                Key=f"datasets/{analysis_id}/{filename}",
                Body=csv)
        except ClientError as e:
            logging.error(e)
            raise e
        return response


    @transaction.atomic
    def update_analysis_dataset(self, analysis_id):
        raise NotImplementedError("Not implemented")
