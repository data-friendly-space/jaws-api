"""This module contains the get roles use case"""
from common.exceptions.exceptions import InternalServerErrorException
from common.use_case.base_use_case import BaseUseCase


class GetRolesUC(BaseUseCase):
    """Retrieves the roles"""
    _instance = None

    def __init__(self):
        if GetRolesUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            GetRolesUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetRolesUC._instance is None:
            GetRolesUC()
        return GetRolesUC._instance

    def exec(self, repository, exclusions):
        """Execute the use case"""
        return repository.get_roles(exclusions)
