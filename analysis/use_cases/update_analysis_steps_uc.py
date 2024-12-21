"""Contains the use case for updating the analysis steps"""
from typing import List
from analysis.contract.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class UpdateAnalysisStepsUC(BaseUseCase):
    """Singleton use case for updating the analysis steps"""
    _instance = None

    def __init__(self):
        if UpdateAnalysisStepsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UpdateAnalysisStepsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if UpdateAnalysisStepsUC._instance is None:
            UpdateAnalysisStepsUC()
        return UpdateAnalysisStepsUC._instance

    def exec(self, repository: AnalysisRepository, analysis_id: int, step_ids: List[int]):
        """Execute the use case"""
        return repository.update_analysis_steps(analysis_id, step_ids)
