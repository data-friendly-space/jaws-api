"""This module contains the get roles use case"""
from common.exceptions.exceptions import InternalServerErrorException
from common.use_case.base_use_case import BaseUseCase
from user_management.contract.repository.role_repository import RoleRepository


class GetRoleByRoleUC(BaseUseCase):
    """Retrieves the roles"""
    _instance = None

    def __init__(self):
        if GetRoleByRoleUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            GetRoleByRoleUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetRoleByRoleUC._instance is None:
            GetRoleByRoleUC()
        return GetRoleByRoleUC._instance

    def exec(self, repository: RoleRepository, role):
        """Execute the use case"""
        return repository.get_role_by_role(role)
