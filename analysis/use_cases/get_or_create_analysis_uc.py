from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetOrCreateAnalysisFrameworkUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetOrCreateAnalysisFrameworkUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetOrCreateAnalysisFrameworkUC._instance = self

    @staticmethod
    def get_instance():
        if GetOrCreateAnalysisFrameworkUC._instance is None:
            GetOrCreateAnalysisFrameworkUC()
        return GetOrCreateAnalysisFrameworkUC._instance

    def exec(self, repository: AnalysisRepository, name):
        return repository.get_or_create_analysis_framework(name)
