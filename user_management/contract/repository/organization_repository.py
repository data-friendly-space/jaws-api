"""This module contains the implementation of organization repository"""
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository
from user_management.contract.io.invite_user_organization_in import InviteUserOrganizationIn
from user_management.contract.to.user_organization_role_to import UserOrganizationRoleTO
from user_management.contract.to.user_organization_to import UserOrganizationTO


class OrganizationRepository(BaseRepository, ABC):
    """Organization repository"""

    @abstractmethod
    def get_user_organizations_by_filters(self, **kwargs) -> list[UserOrganizationRoleTO | None]:
        """Retrieve organization with users and its respective role by filters"""
        pass

    @abstractmethod
    def get_organization_users_by_organization_id(self, organization_id: str) -> list[UserOrganizationTO | None]:
        pass

    @abstractmethod
    def invite_user_to_organization(self, data):
        pass
