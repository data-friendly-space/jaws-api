from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetOrCreateSubPillarUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetOrCreateSubPillarUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetOrCreateSubPillarUC._instance = self

    @staticmethod
    def get_instance():
        if GetOrCreateSubPillarUC._instance is None:
            GetOrCreateSubPillarUC()
        return GetOrCreateSubPillarUC._instance

    def exec(self, repository: AnalysisRepository, name):
        return repository.get_or_create_sub_pillar(name)
