"""Contains the use case for getting a dataset by filename"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.repository.file_management_repository import FileManagementRepository


class GetDatasetByFilenameUC(BaseUseCase):
    """Singleton use case for getting a dataset by filename"""
    _instance = None

    def __init__(self):
        if GetDatasetByFilenameUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDatasetByFilenameUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDatasetByFilenameUC._instance is None:
            GetDatasetByFilenameUC()
        return GetDatasetByFilenameUC._instance

    def exec(self, repository: FileManagementRepository, filename: str) -> DatasetTO:
        dataset = repository.get_dataset_by_filename(filename)
        return dataset
