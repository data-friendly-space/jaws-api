'''This module contains the workspace service'''
from abc import ABC, abstractmethod

from common.helpers.query_options import QueryOptions
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.contract.io.invite_user_workspace_in import InviteUserWorkspaceIn


class WorkspaceService(ABC):
    '''Workspace service'''

    @abstractmethod
    def get_workspaces(self):
        '''Retrieves the workspaces'''
        pass

    @abstractmethod
    def create_workspace(self, request: CreateWorkspaceIn, creator_id: str):
        '''Create a new workspace'''
        pass

    @abstractmethod
    def get_workspaces_by_user_id(self, workspace_id: str, query_options: QueryOptions):
        '''Retrieves the workspaces by user id'''
        pass
