"""Contains the use case for updating the analysis question"""
from typing import List

from analysis.contract.to.analysis_to import AnalysisTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class CreateOrUpdateAnalysisQuestionUC(BaseUseCase):
    """Singleton use case for updating the analysis question"""
    _instance = None

    def __init__(self):
        if CreateOrUpdateAnalysisQuestionUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateOrUpdateAnalysisQuestionUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if CreateOrUpdateAnalysisQuestionUC._instance is None:
            CreateOrUpdateAnalysisQuestionUC()
        return CreateOrUpdateAnalysisQuestionUC._instance

    def exec(self, repository: AnalysisRepository, analysis_id: int, content: str) -> AnalysisTO:
        """Execute the use case"""
        return repository.update_analysis_questions(analysis_id, content)
