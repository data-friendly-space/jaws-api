"""Contains the use case retrieving a subpillar by id"""
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetSubpillarByIdUC(BaseUseCase):
    """Retrieve a subpillar by id"""
    _instance = None

    def __init__(self):
        if GetSubpillarByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetSubpillarByIdUC._instance = self

    @staticmethod
    def get_instance():
        """Return a singleton instance"""
        if GetSubpillarByIdUC._instance is None:
            GetSubpillarByIdUC()
        return GetSubpillarByIdUC._instance

    def exec(self, repository: AnalysisRepository, subpillar_id: int):
        return repository.get_subpillar(subpillar_id)
