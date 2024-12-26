'''This module contains the File Management repository'''
from abc import abstractmethod
from common.repository.base_repository import BaseRepository


class FileManagementRepository(BaseRepository):
    """File Management repository"""
    @abstractmethod
    def create_presigned_url_upload_file(self, filename: str):
        """
        Create a presigned URL to allow the frontend to upload a file
        """

    @abstractmethod
    def attach_dataset_to_analysis(self, analysis_id: int, dataset_reference):
        """Attach a stored dataset with a given analysis

        Keyword arguments:
        analysis_id -- The id of the analysis
        """
