"""Contains the abstract class of file management service"""

from abc import abstractmethod

from common.service.base_service import BaseService


class FileManagementService(BaseService):
    """Service for file management"""

    @abstractmethod
    def create_presigned_url_upload_file(self, user, filename: str):
        """Generate a presigned URL for uplading files"""
