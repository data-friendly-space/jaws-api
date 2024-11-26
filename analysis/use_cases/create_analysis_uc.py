from analysis.contract.repository.analysis_repository import AnalysisRepository
from app.core.use_case.base_use_case import BaseUseCase


class CreateAnalysisUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if CreateAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        if CreateAnalysisUC._instance is None:
            CreateAnalysisUC()
        return CreateAnalysisUC._instance

    def exec(self, repository: AnalysisRepository, scope, disaggregations, sectors):
        return repository.create(scope, disaggregations, sectors)
