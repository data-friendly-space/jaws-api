"""This module contains the get users use case"""
from user_management.contract.repository.organization_repository import OrganizationRepository


class GetAvailableOrganizationsByUserIdUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetAvailableOrganizationsByUserIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAvailableOrganizationsByUserIdUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetAvailableOrganizationsByUserIdUC._instance is None:
            GetAvailableOrganizationsByUserIdUC()
        return GetAvailableOrganizationsByUserIdUC._instance

    def exec(self, repository: OrganizationRepository, user_id: str):
        """Execute the use case"""
        return repository.get_available_organizations_by_user_id(user_id)
