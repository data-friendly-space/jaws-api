from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.contract.to.sector_to import SectorTO
from common.helpers.query_options import QueryOptions
from common.use_case.base_use_case import BaseUseCase


class GetAllSectorsUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetAllSectorsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetAllSectorsUC._instance = self

    @staticmethod
    def get_instance():
        if GetAllSectorsUC._instance is None:
            GetAllSectorsUC()
        return GetAllSectorsUC._instance

    def exec(self, repository: AnalysisRepository, query_options: QueryOptions, **kwargs) -> list[
        SectorTO]:
        return repository.get_all(query_options, **kwargs)
