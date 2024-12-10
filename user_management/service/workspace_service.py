'''This module contains the workspace service'''
from abc import ABC, abstractmethod

from user_management.contract.io.create_workspace_in import CreateWorkspaceIn


class WorkspaceService(ABC):
    '''Workspace service'''

    @abstractmethod
    def get_workspaces(self):
        '''Retrieves the workspaces'''

    @abstractmethod
    def create_workspace(self, request: CreateWorkspaceIn):
        '''Create a new workspace'''

    @abstractmethod
    def get_workspace_users(self, workspace_id):
        '''Create a new workspace'''
