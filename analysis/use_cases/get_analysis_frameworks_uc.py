from analysis.contract.repository.analysis_framework_repository import AnalysisFrameworkRepository
from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from common.helpers.query_options import QueryOptions
from common.use_case.base_use_case import BaseUseCase


class GetAnalysisFrameworkUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetAnalysisFrameworkUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAnalysisFrameworkUC._instance = self

    @staticmethod
    def get_instance():
        if GetAnalysisFrameworkUC._instance is None:
            GetAnalysisFrameworkUC()
        return GetAnalysisFrameworkUC._instance

    def exec(self, repository: AnalysisFrameworkRepository, query_options: QueryOptions, **kwargs) -> list[
        AnalysisFrameworkTO]:
        return repository.get_all(query_options, **kwargs)
