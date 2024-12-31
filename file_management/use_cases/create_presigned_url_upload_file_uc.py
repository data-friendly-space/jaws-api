"""Contains the use case for getting the administrative divisions"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class CreatePresignedUrlUploadFileUC(BaseUseCase):
    """Singleton use case for getting the administrative divisions"""

    _instance = None

    def __init__(self):
        if CreatePresignedUrlUploadFileUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreatePresignedUrlUploadFileUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if CreatePresignedUrlUploadFileUC._instance is None:
            CreatePresignedUrlUploadFileUC()
        return CreatePresignedUrlUploadFileUC._instance

    def exec(
        self,
        repository: FileManagementRepository,
        dataset_id: str,
        user_id: str,
        size_bytes: int,
    ) -> tuple[S3PresignedUrlTO, DatasetTO]:
        presigned_url, dataset = repository.create_presigned_url_upload_file(
            dataset_id, user_id, size_bytes
        )
        return presigned_url, dataset
