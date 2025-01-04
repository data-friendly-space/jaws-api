"""Contains the use case for getting the dataset's file from the storage"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetDatasetFileUC(BaseUseCase):
    """Singleton use case for getting dataset's file from the storage"""

    _instance = None

    def __init__(self):
        if GetDatasetFileUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDatasetFileUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDatasetFileUC._instance is None:
            GetDatasetFileUC()
        return GetDatasetFileUC._instance

    def exec(
        self,
        repository: FileManagementRepository,
        filename: str,
    ) -> dict:
        presigned_url, dataset = repository.get_dataset_file(
            filename
        )
        return presigned_url, dataset
