"""This module contains the get users use case"""
from user_management.contract.repository.organization_repository import OrganizationRepository


class InviteUserToOrganizationUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if InviteUserToOrganizationUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            InviteUserToOrganizationUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if InviteUserToOrganizationUC._instance is None:
            InviteUserToOrganizationUC()
        return InviteUserToOrganizationUC._instance

    def exec(self, repository: OrganizationRepository, data):
        """Execute the use case"""
        return repository.invite_user_to_organization(data)
