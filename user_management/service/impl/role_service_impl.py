"""This module contains the role service Implementation"""
from common.exceptions.exceptions import NotFoundException
from common.use_case.get_all_uc import GetAllUC
from user_management.interfaces.serializers.role_serializer import RoleSerializer
from user_management.repository.role_repository_impl import RoleRepositoryImpl
from user_management.service.role_service import RoleService
from user_management.usecases.get_roles_uc import GetRolesUC


class RoleServiceImpl(RoleService):
    """Role service Implementation"""

    def __init__(self):
        self.get_all_roles_uc = GetAllUC.get_instance()
        self.get_roles_uc = GetRolesUC.get_instance()

    def get_roles(self):
        """Business logic to get roles"""
        roles = self.get_all_roles_uc.exec(RoleRepositoryImpl(), None)
        if not roles:
            raise NotFoundException("Roles not found")
        return [role.to_dict() for role in roles]

    def get_workspace_roles(self):
        """Business logic to get workspace roles"""
        return self.get_roles_uc.exec(RoleRepositoryImpl(), ["ADMIN"])

    def get_analysis_roles(self):
        """Business logic to get analysis roles"""
        return self.get_roles_uc.exec(RoleRepositoryImpl(), ["ADMIN", "FACILITATOR"])

    def get_roles_and_permissions(self):
        """Business logic to get analysis roles"""
        return self.get_roles_uc.exec(RoleRepositoryImpl(), ["ADMIN", "FACILITATOR"])
