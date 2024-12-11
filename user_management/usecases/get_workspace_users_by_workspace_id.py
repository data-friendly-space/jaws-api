"""This module contains the get users use case"""
from user_management.contract.repository.workspace_repository import WorkspaceRepository


class GetWorkspaceUsersByWorkspaceIdUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetWorkspaceUsersByWorkspaceIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetWorkspaceUsersByWorkspaceIdUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetWorkspaceUsersByWorkspaceIdUC._instance is None:
            GetWorkspaceUsersByWorkspaceIdUC()
        return GetWorkspaceUsersByWorkspaceIdUC._instance

    def exec(self, repository: WorkspaceRepository, workspace_id: str):
        """Execute the use case"""
        return repository.get_workspace_users_by_workspace_id(workspace_id)
