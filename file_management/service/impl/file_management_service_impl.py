"""Contains the implementation of AnalysisService"""

import urllib
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException
from file_management.repository.file_management_repository_impl import (
    FileManagementRepositoryImpl,
)
from file_management.service.file_management_service import FileManagementService
from file_management.use_cases.create_dataset_uc import CreateDatasetUC
from file_management.use_cases.create_presigned_url_upload_file_uc import (
    CreatePresignedUrlUploadFileUC,
)
from user_management.repository.role_repository_impl import RoleRepositoryImpl
from user_management.usecases.attach_file_to_analysis_uc import AttachFileToAnalysisUC
from user_management.usecases.get_user_role_in_analysis_uc import (
    GetUserRoleInAnalysisUC,
)


class FileManagementServiceImpl(FileManagementService):
    """Implementation of AnalysisService. Contains the business logic"""

    def __init__(self):
        self.create_presigned_url_upload_file_uc = (
            CreatePresignedUrlUploadFileUC.get_instance()
        )
        self.get_user_role_in_analysis_uc = GetUserRoleInAnalysisUC.get_instance()
        self.attach_file_to_analysis_uc = AttachFileToAnalysisUC.get_instance()
        self.create_dataset_uc = CreateDatasetUC.get_instance()
        self.repository = FileManagementRepositoryImpl()
        self.role_repository = RoleRepositoryImpl()
        self.analysis_service = AnalysisServiceImpl()

    def create_presigned_url_upload_file(
        self, user, filename: str, analysis_id: int
    ) -> str:
        # TODO: validate if the user is in ['FACILITATOR', 'DATA MANAGER']
        self.analysis_service.get_analysis_by_id(
            analysis_id
        )  # Raise 404 if analysis doesn't exist

        response = self.create_presigned_url_upload_file_uc.exec(
            self.repository, filename, analysis_id
        )
        if not response or not response['url'] or not response['fields']:
            raise BadRequestException()
        object_key = urllib.parse.quote(response.fields.key)
        file_url = f"{response.url}{object_key}"

        dataset = self.create_dataset_uc.exec(
            self.repository,
            file_url,
            str(user.id),
            filename)
        self.attach_file_to_analysis_uc.exec(
            self.repository,
            dataset.id,
            analysis_id)

        return response.to_dict()
