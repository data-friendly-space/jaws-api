"""This module contains the get roles use case"""
from common.exceptions.exceptions import InternalServerErrorException
from common.use_case.base_use_case import BaseUseCase
from user_management.contract.repository.organization_repository import OrganizationRepository
from user_management.contract.repository.role_repository import RoleRepository


class GetUserFromOrgByRoleUC(BaseUseCase):
    """Retrieves the roles"""
    _instance = None

    def __init__(self):
        if GetUserFromOrgByRoleUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            GetUserFromOrgByRoleUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetUserFromOrgByRoleUC._instance is None:
            GetUserFromOrgByRoleUC()
        return GetUserFromOrgByRoleUC._instance

    def exec(self, repository: OrganizationRepository, organization_id: str, role_id):
        """Execute the use case"""
        return repository.get_users_from_organization_by_role(organization_id, role_id)
