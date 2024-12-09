"""Contains the use case for adding a administrative divisions into a analysis"""
from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from common.use_case.base_use_case import BaseUseCase


class RemoveLocationUC(BaseUseCase):
    """Singleton use case for removing a administrative divisions from an analysis"""
    _instance = None

    def __init__(self):
        if RemoveLocationUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            RemoveLocationUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if RemoveLocationUC._instance is None:
            RemoveLocationUC()
        return RemoveLocationUC._instance

    def exec(self, repository: AnalysisRepository, analysis: Analysis, location: AdministrativeDivision):
        """Execute the use case"""
        return repository.remove_location(analysis, location)
