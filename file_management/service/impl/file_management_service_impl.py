"""Contains the implementation of AnalysisService"""

from common.exceptions.exceptions import BadRequestException
from file_management.repository.file_management_repository_impl import (
    FileManagementRepositoryImpl,
)
from file_management.service.file_management_service import FileManagementService
from file_management.use_cases.create_presigned_url_upload_file_uc import (
    CreatePresignedUrlUploadFileUC,
)


class FileManagementServiceImpl(FileManagementService):
    """Implementation of AnalysisService. Contains the business logic"""

    def __init__(self):
        self.create_presigned_url_upload_file_uc = CreatePresignedUrlUploadFileUC.get_instance()
        self.repository = FileManagementRepositoryImpl()

    def create_presigned_url_upload_file(self, user, filename: str) -> str:
        # TODO: validate if the user is in ['FACILITATOR', 'DATA MANAGER']
        response = self.create_presigned_url_upload_file_uc.exec(self.repository, filename)
        if not response:
            raise BadRequestException()
        return response.to_dict()
