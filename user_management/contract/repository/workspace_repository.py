"""This module contains the implementation of workspace repository"""
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository
from user_management.contract.to.user_workspace_role_to import UserWorkspaceRoleTO
from user_management.contract.to.user_workspace_to import UserWorkspaceTO


class WorkspaceRepository(BaseRepository, ABC):
    """Workspace repository"""

    @abstractmethod
    def get_user_workspaces_by_filters(self, **kwargs) -> list[UserWorkspaceRoleTO | None]:
        """Retrieve workspace with users and its respective role by filters"""
        pass

    @abstractmethod
    def get_workspace_users_by_workspace_id(self, workspace_id: str) -> list[UserWorkspaceTO | None]:
        pass
