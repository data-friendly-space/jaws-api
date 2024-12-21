"""This module contains the get users use case"""
from user_management.contract.repository.workspace_repository import WorkspaceRepository


class InviteUserToWorkspaceUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if InviteUserToWorkspaceUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            InviteUserToWorkspaceUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if InviteUserToWorkspaceUC._instance is None:
            InviteUserToWorkspaceUC()
        return InviteUserToWorkspaceUC._instance

    def exec(self, repository: WorkspaceRepository, data):
        """Execute the use case"""
        return repository.invite_user_to_workspace(data)
