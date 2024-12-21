"""This module contains the get users use case"""
from user_management.contract.repository.organization_repository import OrganizationRepository


class CreateOrganizationUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if CreateOrganizationUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateOrganizationUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if CreateOrganizationUC._instance is None:
            CreateOrganizationUC()
        return CreateOrganizationUC._instance

    def exec(self, repository: OrganizationRepository, data):
        """Execute the use case"""
        return repository.create(data)
