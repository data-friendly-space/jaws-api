"""This module contains the analysis repository"""

import logging
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
from file_management.contract.dto.dataset_column_to import DatasetColumnTO
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_object_attributes_to import S3ObjectAttributesTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.dto.s3_put_object_to import S3PutObjectTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset
from file_management.models.dataset_column import DatasetColumn
from user_management.models.user import User

bucket_name = getenv("AWS_STORAGE_BUCKET_NAME")


class FileManagementRepositoryImpl(FileManagementRepository):
    """Analysis repository"""

    def create_presigned_url_upload_file(self, external_identifier: str):
        s3_client = boto3.client("s3")
        expires_in = timedelta(hours=1).seconds
        try:
            response = s3_client.generate_presigned_post(
                bucket_name,
                external_identifier,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logging.error(e)
            raise e
        return S3PresignedUrlTO.from_model(response)

    def create_presigned_url_download_file(self, external_identifier: str) -> str:
        s3_client = boto3.client("s3")
        expires_in = timedelta(hours=1).seconds
        try:
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": external_identifier},
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

    def detach_file_from_analysis(self, dataset_id, analysis_id):
        analysis = Analysis.objects.get(id=analysis_id)
        dataset = Dataset.objects.get(id=dataset_id)
        analysis.datasets.remove(dataset)

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

    def get_dataset_file(self, external_identifier):
        s3_client = boto3.client("s3")
        try:
            s3_object = s3_client.get_object(
                Bucket=bucket_name,
                Key=external_identifier
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
            total_columns: int,
            external_identifier):
        user = User.objects.get(id=user_id)
        new_dataset, _ = Dataset.objects.update_or_create(
            url=f"https://{bucket_name}.s3.amazonaws.com/{external_identifier}",
            defaults={
                'filename': filename,
                'size_bytes': size_bytes,
                'uploaded_by': user,
                'mime_type': get_mimetype_from_extension(filename),
                'total_rows': total_rows,
                'total_columns': total_columns,
                'external_identifier': external_identifier
            }
        )
        return DatasetTO.from_model(new_dataset)

    def create_columns(self, dataset_id, columns):
        dataset = Dataset.objects.get(id=dataset_id)
        column_configurations = []
        for col in columns:
            new_column_config, _ = DatasetColumn.objects.update_or_create(
                    dataset=dataset,
                    original_name=col
                )
            column_configurations.append(
                new_column_config
            )
        return DatasetColumnTO.from_models(column_configurations)

    def get_dataset_columns(self, dataset_id):
        columns = DatasetColumn.objects.filter(
            dataset__id=dataset_id
        ).all()
        return DatasetColumnTO.from_models(columns)

    def get_or_create_column_configurations(self, dataset_id, analysis_id):
        analysis = Analysis.objects.get(id=analysis_id)
        columns = DatasetColumn.objects.filter(dataset__id=dataset_id).all()
        column_configurations = []
        for column in columns:
            column_configuration, _ = ColumnConfiguration.objects.get_or_create(
                column=column,
                analysis=analysis)
            column_configurations.append(column_configuration)
        return ColumnConfigurationTO.from_models(column_configurations)

    @transaction.atomic
    def update_columns(self, columns):
        for column in columns.data:
            column_configuration = ColumnConfiguration.objects.get(id=column["id"])
            column_configuration.alias = column["alias"]
            column_configuration.include = column["include"]
            column_configuration.save()

    def create_dataset_file_copy(self, external_identifier, csv) -> S3PutObjectTO:
        s3 = boto3.client("s3")
        try:
            response = s3.put_object(
                Bucket=bucket_name,
                Key=external_identifier,
                Body=csv)
        except ClientError as e:
            logging.error(e)
            raise e
        return S3PutObjectTO.from_model(response)
