"""This module contains the get users use case"""
from user_management.contract.repository.user_repository import UserRepository


class GetUsersUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetUsersUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUsersUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetUsersUC._instance is None:
            GetUsersUC()
        return GetUsersUC._instance

    def exec(self, repository:UserRepository, query_options):
        """Execute the use case"""
        return repository.get_all(query_options)
