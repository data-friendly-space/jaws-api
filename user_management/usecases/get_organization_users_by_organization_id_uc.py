"""This module contains the get users use case"""
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.organization_repository import OrganizationRepository
from user_management.contract.to.user_organization_to import UserOrganizationTO


class GetOrganizationUsersByOrganizationIdUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetOrganizationUsersByOrganizationIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetOrganizationUsersByOrganizationIdUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetOrganizationUsersByOrganizationIdUC._instance is None:
            GetOrganizationUsersByOrganizationIdUC()
        return GetOrganizationUsersByOrganizationIdUC._instance

    def exec(self, repository: OrganizationRepository, query_options: QueryOptions, **kwargs) -> list[UserOrganizationTO]:
        """Execute the use case"""
        return repository.get_organizations_users_by_user_id(query_options, **kwargs)
