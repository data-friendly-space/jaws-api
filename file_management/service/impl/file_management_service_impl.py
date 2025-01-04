"""Contains the implementation of AnalysisService"""

import pandas as pd
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.constants.constants import DATASET_MAX_SIZE, MB
from common.exceptions.exceptions import (
    BadRequestException,
    NotFoundException,
    ForbiddenException,
)
from file_management.repository.file_management_repository_impl import (
    FileManagementRepositoryImpl,
)
from file_management.service.file_management_service import FileManagementService
from file_management.use_cases.create_dataset_column_configurations_uc import (
    CreateDatasetColumnConfigurationsUC,
)
from file_management.use_cases.create_dataset_uc import CreateDatasetUC
from file_management.use_cases.create_presigned_url_download_file_uc import (
    CreatePresignedUrlDownloadFileUC,
)
from file_management.use_cases.create_presigned_url_upload_file_uc import (
    CreatePresignedUrlUploadFileUC,
)
from file_management.use_cases.get_analysis_datasets_uc import GetAnalysisDatasetsUC
from file_management.use_cases.get_dataset_by_filename_uc import GetDatasetByFilenameUC
from file_management.use_cases.get_dataset_file_uc import GetDatasetFileUC
from user_management.repository.role_repository_impl import RoleRepositoryImpl
from user_management.service.impl.users_service_impl import UsersServiceImpl
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
        self.get_analysis_datasets_uc = GetAnalysisDatasetsUC.get_instance()
        self.create_presigned_url_download_file_uc = (
            CreatePresignedUrlDownloadFileUC.get_instance()
        )
        self.create_dataset_column_configurations_uc = (
            CreateDatasetColumnConfigurationsUC.get_instance()
        )
        self.get_dataset_by_filename_uc = (
            GetDatasetByFilenameUC.get_instance()
        )
        self.create_dataset_uc = CreateDatasetUC.get_instance()
        self.get_dataset_file_uc = GetDatasetFileUC.get_instance()
        self.repository = FileManagementRepositoryImpl()
        self.role_repository = RoleRepositoryImpl()
        self.analysis_service = AnalysisServiceImpl()
        self.user_service = UsersServiceImpl()

    def create_presigned_url_upload_file(
        self, user, filename: str, analysis_id
    ) -> str:
        # TODO: validate if the user is in ['FACILITATOR', 'DATA MANAGER']
        # TODO: check if the analysis id is needed to store the dataset in the s3
        presigned_url = self.create_presigned_url_upload_file_uc.exec(
            self.repository, filename
        )
        return presigned_url.to_dict()

    def create_presigned_url_download_file(self, user, dataset_id: str) -> str:
        # TODO: validate if the user have access to the dataset

        dataset = self.repository.get_dataset_by_id(dataset_id)
        if not dataset:
            raise NotFoundException("The dataset doesn't exist")

        response = self.create_presigned_url_download_file_uc.exec(
            self.repository, dataset_id
        )

        if not response:
            raise BadRequestException()
        return response

    def get_analysis_datasets(self, user, analysis_id: int):
        self.analysis_service.get_analysis_by_id(analysis_id)  # Raises 404 if not found
        if not self.user_service.is_user_in_analysis(user.id, analysis_id):
            raise ForbiddenException("You can't see that analysis")
        datasets = self.get_analysis_datasets_uc.exec(self.repository, analysis_id)
        return [dataset.to_dict() for dataset in datasets]

    def confirm_dataset_uploaded(self, user, filename, analysis_id):
        # TODO: Validate the permission of the user
        # Search the dataset in the storage
        dataset_file = self.get_dataset_file_uc.exec(
            self.repository, filename
        )
        # If doesn't exist, raise exception
        if not dataset_file:
            raise NotFoundException("The dataset doesn't exist")

        # If exists create the Dataset record
        size_bytes = dataset_file.ContentLength
        
        if size_bytes > DATASET_MAX_SIZE:
            raise BadRequestException(
                f"The file must be smaller than {DATASET_MAX_SIZE / MB}MB"
            )
        dataset = self.create_dataset_uc.exec(
            self.repository, filename, size_bytes, user.id
        )

        # Attach the dataset to the analysis
        self.attach_file_to_analysis_uc.exec(self.repository, dataset.id, analysis_id)

        # Create the column configurations for each dataset column
        dataset_blob = dataset_file.Body
        dataset_df = pd.read_csv(dataset_blob)
        column_configurations = self.create_dataset_column_configurations_uc.exec(
            self.repository, dataset.id, dataset_df
        )
        return [col.to_dict() for col in column_configurations]
