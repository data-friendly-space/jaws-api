"""This module contains the get users use case"""
from user_management.contract.repository.organization_repository import OrganizationRepository


class GetUserOrganizationsByFiltersUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetUserOrganizationsByFiltersUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUserOrganizationsByFiltersUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetUserOrganizationsByFiltersUC._instance is None:
            GetUserOrganizationsByFiltersUC()
        return GetUserOrganizationsByFiltersUC._instance

    def exec(self, repository: OrganizationRepository, **kwargs):
        """Execute the use case"""
        return repository.get_user_organizations_by_filters(**kwargs)
