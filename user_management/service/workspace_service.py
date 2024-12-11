'''This module contains the workspace service'''
from abc import ABC, abstractmethod

from user_management.contract.io.create_workspace_in import CreateWorkspaceIn


class WorkspaceService(ABC):
    '''Workspace service'''

    @abstractmethod
    def get_workspaces(self):
        '''Retrieves the workspaces'''
        pass

    @abstractmethod
    def create_workspace(self, request: CreateWorkspaceIn):
        '''Create a new workspace'''
        pass

    @abstractmethod
    def get_workspace_users_by_workspace_id(self, workspace_id: str):
        '''Create a new workspace'''
        pass

    @abstractmethod
    def get_workspaces_by_user_id(self, workspace_id):
        pass
