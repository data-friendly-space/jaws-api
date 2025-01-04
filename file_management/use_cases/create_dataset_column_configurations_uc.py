
"""Contains the use case for creating the column configurations of a dataset"""

from pandas import DataFrame
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class CreateDatasetColumnConfigurationsUC(BaseUseCase):
    """Singleton use case for creating the column configurations of a dataset"""

    _instance = None

    def __init__(self):
        if CreateDatasetColumnConfigurationsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateDatasetColumnConfigurationsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if CreateDatasetColumnConfigurationsUC._instance is None:
            CreateDatasetColumnConfigurationsUC()
        return CreateDatasetColumnConfigurationsUC._instance

    def exec(
        self,
        repository: FileManagementRepository,
        dataset_id: str,
        dataset: DataFrame,
    ) -> dict:
        columns = list(dataset.columns)
        column_configurations = repository.create_columns(
            dataset_id,
            columns
        )
        return column_configurations
