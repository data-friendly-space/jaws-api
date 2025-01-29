"""This module contains the get workspace by id uc"""
from user_management.contract.to.workspace_to import WorkspaceTO
from user_management.repository.workspace_repository import WorkspaceRepository


class GetWorkspaceByIdUC:
    """Retrieve the workspace"""
    _instance = None

    def __init__(self):
        if GetWorkspaceByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetWorkspaceByIdUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetWorkspaceByIdUC._instance is None:
            GetWorkspaceByIdUC()
        return GetWorkspaceByIdUC._instance

    def exec(self, repository: WorkspaceRepository, workspace_id: str) -> WorkspaceTO:
        """Execute the use case"""
        return repository.get_by_id(workspace_id)
