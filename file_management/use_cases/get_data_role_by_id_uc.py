"""Contains the use case for getting a data role by id"""

from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.data_role_to import DataRoleTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetDataRoleByIdUC(BaseUseCase):
    """Singleton use case for getting a data role by id"""

    _instance = None

    def __init__(self):
        if GetDataRoleByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDataRoleByIdUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDataRoleByIdUC._instance is None:
            GetDataRoleByIdUC()
        return GetDataRoleByIdUC._instance

    def exec(
        self, repository: FileManagementRepository, data_role_id: int
    ) -> DataRoleTO | None:
        data_role = repository.get_data_type(data_role_id)
        return data_role
