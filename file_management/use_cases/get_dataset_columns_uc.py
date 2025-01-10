"""Contains the use case for getting the columns of a dataset"""

from typing import List
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_column_to import DatasetColumnTO
from file_management.contract.repository.file_management_repository import FileManagementRepository


class GetDatasetColumnsUC(BaseUseCase):
    """Singleton use case for getting the columns of a dataset"""
    _instance = None

    def __init__(self):
        if GetDatasetColumnsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDatasetColumnsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDatasetColumnsUC._instance is None:
            GetDatasetColumnsUC()
        return GetDatasetColumnsUC._instance

    def exec(self, repository: FileManagementRepository, dataset_id: str) -> List[DatasetColumnTO]:
        columns = repository.get_dataset_columns(dataset_id)
        return columns
