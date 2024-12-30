"""This module contains the File Management repository"""

from abc import abstractmethod

from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO


class FileManagementRepository:
    """File Management repository"""

    @abstractmethod
    def create_presigned_url_upload_file(
        self, filename: str, user_id: str
    ) -> tuple[S3PresignedUrlTO, DatasetTO]:
        """
        Create a presigned URL to allow the frontend to upload a file
        """

    @abstractmethod
    def create_presigned_url_download_file(self, dataset_id: str) -> str:
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
    def get_dataset_by_id(self, dataset_id) -> DatasetTO:
        """
        Retrieve a dataset by id
        """
