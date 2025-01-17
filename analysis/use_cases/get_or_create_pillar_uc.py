from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetOrCreatePillarUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetOrCreatePillarUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetOrCreatePillarUC._instance = self

    @staticmethod
    def get_instance():
        if GetOrCreatePillarUC._instance is None:
            GetOrCreatePillarUC()
        return GetOrCreatePillarUC._instance

    def exec(self, repository: AnalysisRepository, name):
        return repository.get_or_create_pillar(name)
