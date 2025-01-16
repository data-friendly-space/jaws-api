"""Contains the use case for getting the datasets of the analysis"""

from typing import List
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetOrCreateColumnConfigurationsTO(BaseUseCase):
    """Singleton use case for getting the datasets of the analysis"""

    _instance = None

    def __init__(self):
        if GetOrCreateColumnConfigurationsTO._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetOrCreateColumnConfigurationsTO._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetOrCreateColumnConfigurationsTO._instance is None:
            GetOrCreateColumnConfigurationsTO()
        return GetOrCreateColumnConfigurationsTO._instance

    def exec(
        self, repository: FileManagementRepository, dataset_id: str, analysis_id: int
    ) -> List[ColumnConfigurationTO]:
        datasets = repository.get_or_create_column_configurations(dataset_id, analysis_id)
        return datasets
