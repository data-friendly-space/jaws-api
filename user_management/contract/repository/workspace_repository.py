"""This module contains the implementation of workspace repository"""
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository, ABC):
    """Workspace repository"""

    @abstractmethod
    def get_workspace_users(self, workspace_id):
        """Retrieve workspace users with its respective role"""
        pass
