"""This module contains the get users use case"""
from user_management.contract.repository.workspace_repository import WorkspaceRepository


class GetUserWorkspacesByFiltersUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetUserWorkspacesByFiltersUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUserWorkspacesByFiltersUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetUserWorkspacesByFiltersUC._instance is None:
            GetUserWorkspacesByFiltersUC()
        return GetUserWorkspacesByFiltersUC._instance

    def exec(self, repository: WorkspaceRepository, **kwargs):
        """Execute the use case"""
        return repository.get_user_workspaces_by_filters(**kwargs)
