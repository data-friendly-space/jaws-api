"""Contains the abstract class of file management service"""

from abc import abstractmethod
from typing import List

from common.helpers.query_options import QueryOptions
from common.service.base_service import BaseService
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.requests.update_columns_in import ColumnIn


class FileManagementService(BaseService):
    """Service for file management"""

    @abstractmethod
    def create_presigned_url_upload_file(self, user, filename: str, analysis_id: int) -> S3PresignedUrlTO:
        """Generate a presigned URL for uplading files"""

    @abstractmethod
    def create_presigned_url_download_file(self, user, dataset_id: str) -> S3PresignedUrlTO:
        """Generate a presigned URL for downloading files"""

    @abstractmethod
    def get_analysis_datasets(self, user, analysis_id: int) -> List[dict]:
        """
        Retrieve all the datasets from the given analysis if the user has the required permissions
        """

    @abstractmethod
    def confirm_dataset_uploaded(self, user, filename: str, analysis_id: int):
        """Validate that the dataset was succesfully uploaded to the storage and if so, create the corresponding column configurations
        Also attach the dataset to the analysis"""

    @abstractmethod
    def get_dataset_columns(self, user, dataset_id: str) -> List[dict]:
        """Retrieve the column configurations for the dataset
        
        Keyword arguments:
        dataset_id -- The id of the dataset
        Return: a list of column configurations
        """

    @abstractmethod
    def get_dataset_rows(self, user, dataset_id: str, query_options: QueryOptions) -> List[dict]:
        """Retrieve the requested rows of the dataset
        
        Keyword arguments:
        user -- The user who requested the rows
        dataset_id -- The id of the dataset
        query_options -- options for pagination and filtering
        Return: A list of rows as dict
        """

    @abstractmethod
    def update_columns(self, user, dataset_id: int, columns: ColumnIn) -> None:
        """Update the given column configurations of a dataset
        
        Keyword arguments:
        user -- The user who is trying to update the columns
        dataset_id -- the id of the dataset
        columns -- The columns with its values
        Return: None
        """
