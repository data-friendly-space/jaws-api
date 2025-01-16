"""This module contains the File Management repository"""

from abc import abstractmethod
from typing import List

from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.dto.data_role_to import DataRoleTO
from file_management.contract.dto.data_type_to import DataTypeTO
from file_management.contract.dto.dataset_column_to import DatasetColumnTO
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO


class FileManagementRepository:
    """File Management repository"""

    @abstractmethod
    def create_presigned_url_upload_file(
        self, external_identifier: str
    ) -> S3PresignedUrlTO:
        """
        Create a presigned URL to allow the frontend to upload a file
        """

    @abstractmethod
    def create_presigned_url_download_file(self, external_identifier: str) -> str:
        """
        Create a presigned URL to allow the frontend download a file
        Returns the url
        """

    @abstractmethod
    def attach_file_to_analysis(self, dataset_id: str, analysis_id: int):
        """Attach a file int an analysis

        Keyword arguments:
        file_url -- the id of the dataset
        analysis_id -- the id of the analysis
        """

    @abstractmethod
    def detach_file_from_analysis(self, dataset_id: str, analysis_id: int) -> None:
        """Detach a file from an analysis
        
        Keyword arguments:
        - dataset_id -- the id of the dataset
        - analysis_id -- the id of the analysis
        Return: None
        """

    @abstractmethod
    def get_dataset_by_id(self, dataset_id) -> DatasetTO:
        """
        Retrieve a dataset by id
        """

    @abstractmethod
    def get_analysis_datasets(self, analysis_id: int) -> List[DatasetTO]:
        """Retrieve the datasets of the analysis
        
        Keyword arguments:
        analysis_id -- the id of the analysis
        Return: A list of DatasetTO
        """

    @abstractmethod
    def get_dataset_by_filename(self, filename: str) -> DatasetTO | None:
        """Search a dataset based on a filename
        
        Keyword arguments:
        filename -- The name to search for
        Return: DatasetTO or None if the dataset was not found
        """
    @abstractmethod
    def get_dataset_file(self, external_identifier: str):
        """Search the dataset in the storage
        
        Keyword arguments:
        external_identifier -- an identifier to get the file from the storage (i.e. Object Key in S3)
        """

    @abstractmethod
    def create_dataset(
        self,
        filename: str,
        size_bytes: int,
        user_id: str,
        total_rows: int,
        total_columns: int,
        external_identifier: str) -> DatasetTO:
        """Create a new Dataset record
        
        Keyword arguments:
         - filename -- The filename of the dataset
         - size_byes -- The size of the file in bytes
         - uder_id -- The id of the user who have uploaded the dataset
         - total_rows -- count of rows
         - total_columns -- count of columns
         - external_identifier -- a identifier of the dataset in the storage provider (i.e. Object Key in S3)
        Return: A data transfer object of the dataset record
        """

    @abstractmethod
    def create_columns(self, dataset_id: str, columns: List[str]) -> List[DatasetColumnTO]:
        """Create the columns of a dataset
        
        Keyword arguments:
        dataset_id -- The id of the dataset
        columns -- List of the column names as string
        """

    @abstractmethod
    def get_dataset_columns(self, dataset_id: str) -> List[DatasetColumnTO]:
        """Find the dataset columns for a given dataset id
        
        Keyword arguments:
        dataset_id -- The id of the dataset
        Return: a list of column configurations
        """

    @abstractmethod
    def get_or_create_column_configurations(
        self,
        dataset_id: int,
        analysis_id: str) -> ColumnConfigurationTO:
        """If exists, retrieve the column configuration for the given column and analysis
        If not, create them
        
        Keyword arguments:
        dataset_id -- The id of the dataset
        analysis_id -- The id of the analysis
        Return: A list of column configurations
        """

    @abstractmethod
    def update_columns(self, columns: List[dict]) -> None:
        """Update dataset columns
        
        Keyword arguments:
        columns -- dict of ColumnsIn 
        Return: None
        """

    @abstractmethod
    def create_dataset_file_copy(self, external_identifier: str, csv: str) -> None:
        """Create a copy of the dataset in the storage
        
        Keyword arguments:
        external_identifier -- The key of the copy dataset
        csv -- The dataset as csv
        Return: None
        """

    @abstractmethod
    def get_data_type(self, data_type_id: int) -> DataTypeTO | None:
        """Get a data type by id
        
        Keyword arguments:
        data_type_id -- the id of the data type
        Return: The data type to or None if not found
        """

    @abstractmethod
    def get_data_role(self, data_role_id: int) -> DataRoleTO | None:
        """Get a data role by id
        
        Keyword arguments:
        data_role_id -- the id of the data role
        Return: The data role to or None if not found
        """

    @abstractmethod
    def get_data_types(self) -> List[DataTypeTO]:
        """Get all the data types
        
        Keyword arguments:
        Return: A list with data types to 
        """

    @abstractmethod
    def get_data_roles(self) -> List[DataRoleTO]:
        """Get all the data roles
        
        Keyword arguments:
        Return: A list with data roles to 
        """
