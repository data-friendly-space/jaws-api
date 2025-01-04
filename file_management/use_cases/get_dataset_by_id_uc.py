"""Contains the use case for getting a dataset by id"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.repository.file_management_repository import FileManagementRepository


class GetDatasetByIdUC(BaseUseCase):
    """Singleton use case for getting a dataset by id"""
    _instance = None

    def __init__(self):
        if GetDatasetByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDatasetByIdUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDatasetByIdUC._instance is None:
            GetDatasetByIdUC()
        return GetDatasetByIdUC._instance

    def exec(self, repository: FileManagementRepository, dataset_id: str) -> DatasetTO | None:
        dataset = repository.get_dataset_by_id(dataset_id)
        return dataset
