"""This module contains the implementation of organization repository"""
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository
from user_management.contract.to.organization_to import OrganizationTO


class OrganizationRepository(BaseRepository, ABC):
    """Organization repository"""

    @abstractmethod
    def get_organizations_by_filters(self, **kwargs) -> list[OrganizationTO | None]:
        """Retrieve organizations with users and its respective role by filters"""
        pass
