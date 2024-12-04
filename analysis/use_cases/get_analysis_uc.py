from analysis.contract.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetAnalysisUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        if GetAnalysisUC._instance is None:
            GetAnalysisUC()
        return GetAnalysisUC._instance

    def exec(self, repository: AnalysisRepository):
        return repository.get_all()
