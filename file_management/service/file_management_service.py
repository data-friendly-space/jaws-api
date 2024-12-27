"""Contains the abstract class of file management service"""

from abc import abstractmethod

from common.service.base_service import BaseService
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO


class FileManagementService(BaseService):
    """Service for file management"""

    @abstractmethod
    def create_presigned_url_upload_file(self, user, filename: str) -> S3PresignedUrlTO:
        """Generate a presigned URL for uplading files"""

    @abstractmethod
    def create_presigned_url_download_file(self, user, dataset_id: str) -> S3PresignedUrlTO:
        """Generate a presigned URL for downloading files"""
