"""This module contains the implementation of organization repository"""
from abc import ABC, abstractmethod

from common.helpers.query_options import QueryOptions
from common.repository.base_repository import BaseRepository
from user_management.contract.to.user_organization_role_to import UserOrganizationRoleTO
from user_management.contract.to.user_organization_to import UserOrganizationTO


class OrganizationRepository(BaseRepository, ABC):
    """Organization repository"""

    @abstractmethod
    def get_user_organizations_by_filters(self, query_options: QueryOptions, **kwargs) -> list[UserOrganizationRoleTO | None]:
        """Retrieve organization with users and its respective role by filters"""
        pass

    @abstractmethod
    def get_organizations_users_by_user_id(self, query_options: QueryOptions, **kwargs) -> list[UserOrganizationTO]:
        pass


    @abstractmethod
    def get_available_organizations_by_user_id(self, user_id: str):
        pass

    @abstractmethod
    def get_users_from_organization_by_role(self, organization_id: str, role_id: str):
        pass
