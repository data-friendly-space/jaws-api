"""Contains the use case for getting all the data roles"""

from typing import List
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.data_role_to import DataRoleTO
from file_management.contract.repository.file_management_repository import (
    FileManagementRepository,
)


class GetDataRolesUC(BaseUseCase):
    """Singleton use case for getting all the data roles"""

    _instance = None

    def __init__(self):
        if GetDataRolesUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDataRolesUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDataRolesUC._instance is None:
            GetDataRolesUC()
        return GetDataRolesUC._instance

    def exec(self, repository: FileManagementRepository) -> List[DataRoleTO]:
        data_roles = repository.get_data_roles()
        return data_roles
