"""Contains the use case for getting a data type by id"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.data_type_to import DataTypeTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetDataTypeByIdUC(BaseUseCase):
    """Singleton use case for getting a data type by id"""

    _instance = None

    def __init__(self):
        if GetDataTypeByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDataTypeByIdUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDataTypeByIdUC._instance is None:
            GetDataTypeByIdUC()
        return GetDataTypeByIdUC._instance

    def exec(
        self, repository: FileManagementRepository, data_type_id: int
    ) -> DataTypeTO | None:
        data_type = repository.get_data_type(data_type_id)
        return data_type
