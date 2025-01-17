from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.helpers.query_options import QueryOptions
from common.use_case.base_use_case import BaseUseCase


class GetAllDisaggregationsUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetAllDisaggregationsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAllDisaggregationsUC._instance = self

    @staticmethod
    def get_instance():
        if GetAllDisaggregationsUC._instance is None:
            GetAllDisaggregationsUC()
        return GetAllDisaggregationsUC._instance

    def exec(self, repository: AnalysisRepository, query_options: QueryOptions, **kwargs) -> list[
        DisaggregationTO]:
        return repository.get_all_disaggregations(query_options, **kwargs)
