"""Contains the use case for getting the administrative divisions"""
from analysis.contract.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetAdministrativeDivisionsUC(BaseUseCase):
    """Singleton use case for getting the administrative divisions"""
    _instance = None

    def __init__(self):
        if GetAdministrativeDivisionsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAdministrativeDivisionsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetAdministrativeDivisionsUC._instance is None:
            GetAdministrativeDivisionsUC()
        return GetAdministrativeDivisionsUC._instance

    def exec(self, repository: AnalysisRepository, parent_p_code):
        """Execute the use case"""
        return repository.get_administrative_divisions(parent_p_code)
