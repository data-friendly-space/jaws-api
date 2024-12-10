"""This module contains the get users use case"""
from user_management.contract.repository.workspace_repository import WorkspaceRepository


class CreateWorkspaceUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if CreateWorkspaceUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateWorkspaceUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if CreateWorkspaceUC._instance is None:
            CreateWorkspaceUC()
        return CreateWorkspaceUC._instance

    def exec(self, repository:WorkspaceRepository, data):
        """Execute the use case"""
        return repository.create(data)
