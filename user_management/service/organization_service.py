'''This module contains the organization service'''
from abc import ABC, abstractmethod

from user_management.contract.io.create_organization_in import CreateOrganizationIn


class OrganizationService(ABC):
    '''Organization service'''

    @abstractmethod
    def get_organizations(self):
        '''Retrieves the organizations'''

    @abstractmethod
    def create_organization(self, request: CreateOrganizationIn):
        '''Create a new organization'''

    @abstractmethod
    def get_organization_users_by_organization_id(self, organization_id: str):
        '''Retrieves the organization users by organization id'''
        pass

    @abstractmethod
    def get_organizations_by_user_id(self, user_id):
        '''Retrieves the organizations by user id'''
        pass
