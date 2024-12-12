'''This module contains the workspace service'''
from abc import ABC, abstractmethod

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
    def get_workspace_users_by_workspace_id(self, workspace_id: str):
        '''Retrieves the workspace users by workspace id'''
        pass

    @abstractmethod
    def get_workspaces_by_user_id(self, workspace_id):
        '''Retrieves the workspaces by user id'''
        pass

    @abstractmethod
    def invite_user_to_workspace(self, invite_user_in: InviteUserWorkspaceIn):
        '''Invite user with role to workspace '''
        pass

