"""This module contains the implementation of workspace repository"""
from abc import ABC, abstractmethod

from common.helpers.query_options import QueryOptions
from common.repository.base_repository import BaseRepository
from user_management.contract.to.user_workspace_role_to import UserWorkspaceRoleTO
from user_management.contract.to.user_workspace_to import UserWorkspaceTO


class WorkspaceRepository(BaseRepository, ABC):
    """Workspace repository"""

    @abstractmethod
    def get_user_workspaces_by_filters(self, query_options: QueryOptions, **kwargs) -> list[UserWorkspaceRoleTO]:
        """Retrieve workspaces relate to the user"""
        pass

    @abstractmethod
    def get_workspaces_users_by_user_id(self, workspace_id: str) -> list[UserWorkspaceTO | None]:
        """Retrieve users relate to the workspace"""
        pass

    @abstractmethod
    def invite_user_to_workspace(self, data):
        """Invite user to workspace"""
        pass

    @abstractmethod
    def add_user_to_workspace(self, user_id, workspace_id, role_id) -> UserWorkspaceRoleTO | None:
        """add user to workspace"""
        pass
