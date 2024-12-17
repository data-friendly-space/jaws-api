'''This module contains the organization service'''
from abc import ABC, abstractmethod

from common.helpers.query_options import QueryOptions
from user_management.contract.io.create_organization_in import CreateOrganizationIn
from user_management.contract.io.invite_user_organization_in import InviteUserOrganizationIn


class OrganizationService(ABC):
    '''Organization service'''

    @abstractmethod
    def get_organizations(self):
        '''Retrieves the organizations'''

    @abstractmethod
    def create_organization(self, request: CreateOrganizationIn):
        '''Create a new organization'''

    @abstractmethod
    def get_organizations_users_by_user_id(self, user_id: str, query_options: QueryOptions):
        '''Retrieves the organization users by user id'''
        pass

    @abstractmethod
    def get_organizations_by_user_id(self, query_options: QueryOptions, user_id: str):
        '''Retrieves the organizations by user id'''
        pass


    @abstractmethod
    def get_available_organizations_by_user_id(self, **kwargs):
        pass

    @abstractmethod
    def get_organization_users_by_role(self, organization_id: str, role: str):
        pass
