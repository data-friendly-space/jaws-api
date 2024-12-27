"""Contains the use case for creating datasets"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class CreateDatasetUC(BaseUseCase):
    """Singleton use case for creating datasets"""

    _instance = None

    def __init__(self):
        if CreateDatasetUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateDatasetUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if CreateDatasetUC._instance is None:
            CreateDatasetUC()
        return CreateDatasetUC._instance

    def exec(
        self,
        repository: FileManagementRepository,
        url: str,
        user_id: str,
        filename: str,
    ) -> DatasetTO:
        dataset_id = repository.create_dataset(url, user_id, filename)
        return dataset_id
