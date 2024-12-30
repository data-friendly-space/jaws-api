"""Contains the use case for creating a presigned url to download files"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import FileManagementRepository


class CreatePresignedUrlDownloadFileUC(BaseUseCase):
    """Singleton use case for creating a presigned url to download files"""
    _instance = None

    def __init__(self):
        if CreatePresignedUrlDownloadFileUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreatePresignedUrlDownloadFileUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if CreatePresignedUrlDownloadFileUC._instance is None:
            CreatePresignedUrlDownloadFileUC()
        return CreatePresignedUrlDownloadFileUC._instance

    def exec(self, repository: FileManagementRepository, dataset_id: str) -> S3PresignedUrlTO:
        presigned_url = repository.create_presigned_url_download_file(dataset_id)
        return presigned_url
