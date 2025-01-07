"""Contains the use case for getting the administrative divisions"""
from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetAdministrativeDivisionByPCodeUC(BaseUseCase):
    """Singleton use case for getting the administrative divisions"""
    _instance = None

    def __init__(self):
        if GetAdministrativeDivisionByPCodeUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAdministrativeDivisionByPCodeUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetAdministrativeDivisionByPCodeUC._instance is None:
            GetAdministrativeDivisionByPCodeUC()
        return GetAdministrativeDivisionByPCodeUC._instance

    def exec(self, repository: AnalysisRepository, p_code) -> AdministrativeDivisionTO:
        """Execute the use case"""
        return repository.get_administrative_division(p_code)
