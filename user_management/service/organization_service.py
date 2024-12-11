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
    def get_organization_users(self, organization_id):
        '''Create a new organization'''
