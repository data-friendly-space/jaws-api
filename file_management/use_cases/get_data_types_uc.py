"""Contains the use case for getting all the data types"""

from typing import List
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.data_type_to import DataTypeTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetDataTypesUC(BaseUseCase):
    """Singleton use case for getting all the data types"""

    _instance = None

    def __init__(self):
        if GetDataTypesUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDataTypesUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDataTypesUC._instance is None:
            GetDataTypesUC()
        return GetDataTypesUC._instance

    def exec(self, repository: FileManagementRepository) -> List[DataTypeTO]:
        data_types = repository.get_data_types()
        return data_types
