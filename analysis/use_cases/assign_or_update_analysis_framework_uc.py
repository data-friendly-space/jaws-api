"""Contains the use case for updating the analysis framework"""
from typing import List

from analysis.contract.to.analysis_to import AnalysisTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class AssignOrUpdateAnalysisFrameworkUC(BaseUseCase):
    """Singleton use case for updating the analysis framework"""
    _instance = None

    def __init__(self):
        if AssignOrUpdateAnalysisFrameworkUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AssignOrUpdateAnalysisFrameworkUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if AssignOrUpdateAnalysisFrameworkUC._instance is None:
            AssignOrUpdateAnalysisFrameworkUC()
        return AssignOrUpdateAnalysisFrameworkUC._instance

    def exec(self, repository: AnalysisRepository, analysis_id: int, framework_id: int) -> AnalysisTO :
        """Execute the use case"""
        return repository.assign_or_update_framework_to_analysis(analysis_id, framework_id)
