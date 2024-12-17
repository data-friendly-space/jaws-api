"""This module contains the get users use case"""
from user_management.contract.repository.workspace_repository import WorkspaceRepository
from user_management.contract.to.user_workspace_role_to import UserWorkspaceRoleTO


class AddUserToWorkspaceUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if AddUserToWorkspaceUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AddUserToWorkspaceUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if AddUserToWorkspaceUC._instance is None:
            AddUserToWorkspaceUC()
        return AddUserToWorkspaceUC._instance

    def exec(self, repository: WorkspaceRepository, user_id, workspace_id, role_id) -> UserWorkspaceRoleTO | None:
        """Execute the use case"""
        return repository.add_user_to_workspace(user_id, workspace_id, role_id)
