"""Contains the use case for storing a new dataset in the fileserver"""

from typing import List

import pandas as pd
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class StoreDatasetUC(BaseUseCase):
    """Singleton use case for storing a dataset"""

    _instance = None

    def __init__(self):
        if StoreDatasetUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            StoreDatasetUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if StoreDatasetUC._instance is None:
            StoreDatasetUC()
        return StoreDatasetUC._instance

    def exec(
        self, repository: FileManagementRepository, dataset: pd.DataFrame, external_identifier: str
    ) -> List[ColumnConfigurationTO]:
        response = repository.store_dataset(dataset, external_identifier)
        return response
