"""Contains the implementation of AnalysisService"""

import urllib

import pandas as pd

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.constants.constants import DATASET_MAX_SIZE, MB
from common.exceptions.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from common.helpers.query_options import QueryOptions
from file_management.repository.file_management_repository_impl import (
    FileManagementRepositoryImpl,
)
from file_management.service.file_management_service import FileManagementService
from file_management.use_cases.create_dataset_column_configurations_uc import (
    CreateDatasetColumnConfigurationsUC,
)
from file_management.use_cases.create_dataset_copy_uc import CreateDatasetCopyUC
from file_management.use_cases.create_dataset_uc import CreateDatasetUC
from file_management.use_cases.create_presigned_url_download_file_uc import (
    CreatePresignedUrlDownloadFileUC,
)
from file_management.use_cases.create_presigned_url_upload_file_uc import (
    CreatePresignedUrlUploadFileUC,
)
from file_management.use_cases.get_analysis_datasets_uc import GetAnalysisDatasetsUC
from file_management.use_cases.get_data_role_by_id_uc import GetDataRoleByIdUC
from file_management.use_cases.get_data_type_by_id_uc import GetDataTypeByIdUC
from file_management.use_cases.get_dataset_by_filename_uc import GetDatasetByFilenameUC
from file_management.use_cases.get_dataset_by_id_uc import GetDatasetByIdUC
from file_management.use_cases.get_dataset_columns_uc import GetDatasetColumnsUC
from file_management.use_cases.get_dataset_file_uc import GetDatasetFileUC
from file_management.use_cases.get_dataset_rows_uc import GetDatasetRowsUC
from file_management.use_cases.get_data_types_uc import GetDataTypesUC
from file_management.use_cases.get_data_roles_uc import GetDataRolesUC
from file_management.use_cases.get_or_create_column_configurations_uc import (
    GetOrCreateColumnConfigurationsTO,
)
from file_management.use_cases.update_columns_uc import UpdateColumnsUC
from user_management.repository.impl.role_repository_impl import RoleRepositoryImpl
from user_management.service.impl.users_service_impl import UsersServiceImpl
from user_management.usecases.attach_file_to_analysis_uc import AttachFileToAnalysisUC
from user_management.usecases.detach_file_from_analysis_uc import (
    DetachFileFromAnalysisUC,
)
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
        self.detach_file_from_analysis_uc = DetachFileFromAnalysisUC.get_instance()
        self.get_analysis_datasets_uc = GetAnalysisDatasetsUC.get_instance()
        self.create_presigned_url_download_file_uc = (
            CreatePresignedUrlDownloadFileUC.get_instance()
        )
        self.create_dataset_columns = CreateDatasetColumnConfigurationsUC.get_instance()
        self.get_dataset_by_filename_uc = GetDatasetByFilenameUC.get_instance()
        self.create_dataset_uc = CreateDatasetUC.get_instance()
        self.get_dataset_file_uc = GetDatasetFileUC.get_instance()
        self.get_dataset_columns_uc = GetDatasetColumnsUC.get_instance()
        self.get_dataset_by_id_uc = GetDatasetByIdUC.get_instance()
        self.get_data_type_by_id_uc = GetDataTypeByIdUC.get_instance()
        self.get_data_role_by_id_uc = GetDataRoleByIdUC.get_instance()
        self.get_data_types_uc = GetDataTypesUC.get_instance()
        self.get_data_roles_uc = GetDataRolesUC.get_instance()
        self.get_dataset_rows_uc = GetDatasetRowsUC.get_instance()
        self.update_columns_uc = UpdateColumnsUC.get_instance()
        self.create_dataset_copy_uc = CreateDatasetCopyUC.get_instance()
        self.get_or_create_column_configurations = (
            GetOrCreateColumnConfigurationsTO.get_instance()
        )
        self.repository = FileManagementRepositoryImpl()
        self.role_repository = RoleRepositoryImpl()
        self.analysis_service = AnalysisServiceImpl()
        self.user_service = UsersServiceImpl()

    def create_presigned_url_upload_file(self, user, filename: str, analysis_id) -> str:
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
            self.repository, dataset.externalIdentifier
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
            self.repository, urllib.parse.quote(f"datasets/{filename}")
        )
        # If doesn't exist, raise exception
        if not dataset_file:
            raise NotFoundException("The dataset doesn't exist")

        # If exists create the Dataset record
        size_bytes = dataset_file.ContentLength
        dataset_blob = dataset_file.Body
        dataset_df = pd.read_csv(dataset_blob)

        total_rows = len(dataset_df)
        total_columns = len(dataset_df.columns)

        if size_bytes > DATASET_MAX_SIZE:
            raise BadRequestException(
                f"The file must be smaller than {DATASET_MAX_SIZE / MB}MB"
            )
        dataset = self.create_dataset_uc.exec(
            self.repository,
            filename,
            size_bytes,
            user.id,
            total_rows,
            total_columns,
            urllib.parse.quote(f"datasets/{filename}"),
        )
        # Create the dataset columns
        columns = self.create_dataset_columns.exec(
            self.repository, dataset.id, dataset_df
        )

        # Attach the dataset to the analysis
        self.attach_file_to_analysis_uc.exec(self.repository, dataset.id, analysis_id)

        return [col.to_dict() for col in columns]

    def get_dataset_columns(self, user, dataset_id):
        # TODO: validate if the user can see the dataset
        dataset = self.get_dataset_by_id_uc.exec(self.repository, dataset_id)
        if not dataset:
            raise NotFoundException("The dataset doesn't exist.")
        columns = self.get_dataset_columns_uc.exec(self.repository, dataset_id)
        return [col.to_dict() for col in columns]

    def get_column_configurations(self, user, dataset_id, analysis_id):
        # TODO: validate if the user can see the dataset
        dataset = self.get_dataset_by_id_uc.exec(self.repository, dataset_id)
        if not dataset:
            raise NotFoundException("The dataset doesn't exist.")
        column_configurations = self.get_or_create_column_configurations.exec(
            self.repository, dataset_id, analysis_id
        )
        return [col.to_dict() for col in column_configurations]

    def get_dataset_rows(self, user, dataset_id, query_options):
        dataset = self.get_dataset_by_id_uc.exec(self.repository, dataset_id)
        if not dataset:
            raise NotFoundException("The dataset doesn't exist.")

        dataset_file = self.get_dataset_file_uc.exec(
            self.repository, dataset.externalIdentifier
        )

        rows = self.get_dataset_rows_uc.exec(dataset_file, query_options)
        return rows

    def update_columns(self, user, dataset_id, columns):
        # TODO: Check if the user can update the column configurations
        for column in columns:
            if not column["subpillar_id"]:
                continue
            data_role = self.get_data_role_by_id_uc.exec(
                self.repository, column["data_role_id"]
            )
            if data_role.name != "Content":
                raise BadRequestException(
                    "You can't add a column pillar if the data role is different of content"
                )
        dataset = self.get_dataset_by_id_uc.exec(self.repository, dataset_id)
        if not dataset:
            raise NotFoundException("The dataset doesn't exist")
        self.update_columns_uc.exec(self.repository, columns)

    def update_rows(self, user, dataset_id, rows):
        # TODO: Validate if the user can update the rows
        analysis_id = rows.validated_data["analysis_id"]
        dataset = self.get_dataset_by_id_uc.exec(self.repository, dataset_id)
        if not dataset:
            raise NotFoundException("The dataset doesn't exist")

        dataset_file = self.get_dataset_file_uc.exec(
            self.repository, dataset.externalIdentifier
        )
        dataset_blob = dataset_file.Body
        dataset_dataframe = pd.read_csv(dataset_blob)
        start_row = (
            rows.validated_data["page_size"] * (rows.validated_data["page_number"] - 1)
            + 1
        )
        end_row = rows.validated_data["page_size"] * rows.validated_data["page_number"]

        external_identifier = urllib.parse.quote(
            f"datasets/{analysis_id}/{dataset.filename}"
        )

        _, new_csv = self.create_dataset_copy_uc.exec(
            self.repository,
            dataset_dataframe,
            start_row,
            end_row,
            rows.validated_data["rows"],
            external_identifier,
        )
        new_file_size = len(new_csv.encode("utf-8"))
        if new_file_size > DATASET_MAX_SIZE:
            raise BadRequestException(
                f"The file must be smaller than {DATASET_MAX_SIZE / MB}MB"
            )
        dataset_copy = self.create_dataset_uc.exec(
            self.repository,
            dataset.filename,
            new_file_size,
            user.id,
            len(dataset_dataframe),
            len(dataset_dataframe.columns),
            external_identifier,
        )

        self.create_dataset_columns.exec(
            self.repository, dataset_copy.id, dataset_dataframe
        )

        self.detach_file_from_analysis_uc.exec(self.repository, dataset_id, analysis_id)

        self.attach_file_to_analysis_uc.exec(
            self.repository, dataset_copy.id, analysis_id
        )

    def get_data_types(self):
        data_types = self.get_data_types_uc.exec(self.repository)
        return [data_type.to_dict() for data_type in data_types]

    def get_data_roles(self):
        data_roles = self.get_data_roles_uc.exec(self.repository)
        return [data_role.to_dict() for data_role in data_roles]

    def get_merge_preview(self, user, merge_config):
        data_frames = []
        merged_df = None
        join_column = merge_config["datasets"][0]["join_column"]
        for dataset_join_config in merge_config["datasets"]:
            dataset = self.get_dataset_by_id_uc.exec(
                self.repository, dataset_join_config["id"]
            )
            dataset_file = self.get_dataset_file_uc.exec(
                self.repository, dataset.externalIdentifier
            )
            try:
                df = pd.read_csv(dataset_file.Body)
                data_frames.append(df)
            except pd.errors.ParserError:
                df = pd.read_csv(dataset_file.Body, sep=";")

            if merged_df is None:
                merged_df = df
            else:
                try:
                    merged_df = merged_df.merge(
                        df,
                        left_on=join_column,
                        right_on=dataset_join_config["join_column"],
                        how=merge_config["method"],
                    )
                except ValueError as e:
                    raise BadRequestException(
                        "The columns you've selected as join columns doesn't match or contains different types, check the data and try again"
                    ) from e

        # Fill string columns
        merged_df[merged_df.select_dtypes(include="object").columns] = (
            merged_df.select_dtypes(include="object").fillna("")
        )

        # Fill numeric columns
        merged_df[merged_df.select_dtypes(include="number").columns] = (
            merged_df.select_dtypes(include="number").fillna(0)
        )

        merged_df.fillna("", inplace=True)

        query_options = QueryOptions(
            page_number=1,
            page_size=10,
        )
        return query_options.paginate_and_filter_dataframe(merged_df)
