"""Contains the use case for getting the steps"""
from analysis.contract.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetStepsUC(BaseUseCase):
    """Retrieve the analysis steps"""
    _instance = None

    def __init__(self):
        if GetStepsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetStepsUC._instance = self

    @staticmethod
    def get_instance():
        """Return a singleton instance"""
        if GetStepsUC._instance is None:
            GetStepsUC()
        return GetStepsUC._instance

    def exec(self, repository: AnalysisRepository):
        return repository.get_steps()
