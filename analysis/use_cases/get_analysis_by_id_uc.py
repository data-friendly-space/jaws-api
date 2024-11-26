from analysis.contract.repository.analysis_repository import AnalysisRepository
from app.core.use_case.base_use_case import BaseUseCase


class GetAnalysisByIdUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetAnalysisByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAnalysisByIdUC._instance = self

    @staticmethod
    def get_instance():
        if GetAnalysisByIdUC._instance is None:
            GetAnalysisByIdUC()
        return GetAnalysisByIdUC._instance

    def exec(self, repository: AnalysisRepository, id: str):
        return repository.get_by_id(id)
