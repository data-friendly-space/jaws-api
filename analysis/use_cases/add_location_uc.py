"""Contains the use case for adding a administrative divisions into a analysis"""
from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from common.use_case.base_use_case import BaseUseCase


class AddLocationUC(BaseUseCase):
    """Singleton use case for adding a administrative divisions into a analysis"""
    _instance = None

    def __init__(self):
        if AddLocationUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AddLocationUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if AddLocationUC._instance is None:
            AddLocationUC()
        return AddLocationUC._instance

    def exec(self, repository: AnalysisRepository, analysis: Analysis, location: AdministrativeDivision):
        """Execute the use case"""
        return repository.add_location(analysis, location)
