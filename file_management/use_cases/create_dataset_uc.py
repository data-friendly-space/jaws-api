
"""Contains the use case for creating a dataset"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.dataset_to import DatasetTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class CreateDatasetUC(BaseUseCase):
    """Singleton use case for creating a dataset"""

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
        filename: str,
        size_bytes: int,
        user_id: str,
        total_rows: int,
        total_columns: int,
        external_identifier: str
    ) -> DatasetTO:
        dataset = repository.create_dataset(
            filename,
            size_bytes,
            user_id,
            total_rows,
            total_columns,
            external_identifier
        )
        return dataset
