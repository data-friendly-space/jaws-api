"""Contains the use case for updating dataset columns"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.repository.file_management_repository import FileManagementRepository


class UpdateColumnsUC(BaseUseCase):
    """Singleton use case for updating dataset columns"""
    _instance = None

    def __init__(self):
        if UpdateColumnsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UpdateColumnsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if UpdateColumnsUC._instance is None:
            UpdateColumnsUC()
        return UpdateColumnsUC._instance

    def exec(
            self,
            repository: FileManagementRepository,
            columns
        ) -> None:
        repository.update_columns(columns)
