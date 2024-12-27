'''This module contains the File Management repository'''
from abc import abstractmethod

from file_management.contract.dto.dataset_to import DatasetTO


class FileManagementRepository:
    """File Management repository"""
    @abstractmethod
    def create_presigned_url_upload_file(self, filename: str, analysis_id: int):
        """
        Create a presigned URL to allow the frontend to upload a file
        """

    @abstractmethod
    def attach_file_to_analysis(self, dataset_id: str, analysis_id: int):
        """Attach a file int an analysis
        
        Keyword arguments:
        file_url -- the id of the dataset
        analysis_id -- the id of the analysis
        """

    @abstractmethod
    def create_dataset(self, file_url: str, user_id: str, filename: str) -> DatasetTO:
        """Create a new Dataset
        
        Keyword arguments:
        file_url -- the url of the dataset
        filename -- the filename
        user_id -- the id of the user who have uploaded the dataset
        """
