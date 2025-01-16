"""Contains the use case for adding a administrative divisions into a analysis"""
from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.contract.to.analysis_to import AnalysisTO
from analysis.repository.analysis_repository import AnalysisRepository
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

    def exec(self, repository: AnalysisRepository, analysis: AnalysisTO, location: AdministrativeDivisionTO):
        """Execute the use case"""
        return repository.add_location(analysis, location)
