"""This module contains the get users use case"""
from user_management.contract.repository.user_repository import UserRepository


class GetUserByFiltersUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetUserByFiltersUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUserByFiltersUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetUserByFiltersUC._instance is None:
            GetUserByFiltersUC()
        return GetUserByFiltersUC._instance

    def exec(self, repository: UserRepository, **kwargs):
        """Execute the use case"""
        return repository.get_user_by_filters(**kwargs)
