"""Contains the use case for getting the datasets of the analysis"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetAnalysisDatasetsUC(BaseUseCase):
    """Singleton use case for getting the datasets of the analysis"""

    _instance = None

    def __init__(self):
        if GetAnalysisDatasetsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAnalysisDatasetsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetAnalysisDatasetsUC._instance is None:
            GetAnalysisDatasetsUC()
        return GetAnalysisDatasetsUC._instance

    def exec(
        self, repository: FileManagementRepository, analysis_id: int
    ) -> tuple[S3PresignedUrlTO, DatasetTO]:
        datasets = repository.get_analysis_datasets(analysis_id)
        if not datasets:
            return []
        return datasets
