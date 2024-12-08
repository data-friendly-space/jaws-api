'''This module contains the workspace service'''
from abc import ABC, abstractmethod


class WorkspaceService(ABC):
    '''Workspace service'''
    @abstractmethod
    def get_workspaces(self):
        '''Retrieves the workspaces'''

    @abstractmethod
    def create_workspace(self, name, lastname, email, password):
        '''Create a new user'''

