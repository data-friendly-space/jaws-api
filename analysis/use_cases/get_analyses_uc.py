from analysis.repository.analysis_repository import AnalysisRepository
from common.helpers.query_options import QueryOptions
from common.use_case.base_use_case import BaseUseCase


class GetAnalysesUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetAnalysesUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAnalysesUC._instance = self

    @staticmethod
    def get_instance():
        if GetAnalysesUC._instance is None:
            GetAnalysesUC()
        return GetAnalysesUC._instance

    def exec(self, repository: AnalysisRepository, query_options: QueryOptions, **kwargs):
        return repository.get_all(query_options, **kwargs)
