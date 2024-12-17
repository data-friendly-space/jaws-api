"""This module contains the get models use case"""
from common.exceptions.exceptions import InternalServerErrorException
from common.helpers.query_options import QueryOptions
from common.use_case.base_use_case import BaseUseCase


class GetAllUC(BaseUseCase):
    """Retrieves the models"""
    _instance = None

    def __init__(self):
        if GetAllUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            GetAllUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetAllUC._instance is None:
            GetAllUC()
        return GetAllUC._instance

    def exec(self, repository, query_options: QueryOptions):
        """Execute the use case"""
        return repository.get_all(query_options)
