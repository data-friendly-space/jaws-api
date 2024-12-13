'''This module contains the role service'''
from abc import ABC, abstractmethod


class RoleService(ABC):
    '''Role service'''

    @abstractmethod
    def get_roles(self):
        '''Retrieves the roles'''

    @abstractmethod
    def get_workspace_roles(self):
        '''Retrieves the roles'''

    @abstractmethod
    def get_analysis_roles(self):
        '''Retrieves the roles'''
    @abstractmethod
    def get_roles_and_permissions(self):
        pass