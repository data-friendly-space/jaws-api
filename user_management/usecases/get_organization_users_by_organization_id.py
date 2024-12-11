"""This module contains the get users use case"""
from user_management.contract.repository.organization_repository import OrganizationRepository


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

    def exec(self, repository: OrganizationRepository, organization_id: str):
        """Execute the use case"""
        return repository.get_organization_users_by_organization_id(organization_id)
