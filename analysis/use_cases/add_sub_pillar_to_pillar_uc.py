from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.contract.to.pillar_to import PillarTO
from analysis.contract.to.sub_pillar_to import SubPillarTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class AddSubPillarToPillarUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if AddSubPillarToPillarUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AddSubPillarToPillarUC._instance = self

    @staticmethod
    def get_instance():
        if AddSubPillarToPillarUC._instance is None:
            AddSubPillarToPillarUC()
        return AddSubPillarToPillarUC._instance

    def exec(self, repository: AnalysisRepository, pillar_id: int, sub_pillar:SubPillarTO) -> PillarTO:
        return repository.add_sub_pillar_to_pillar(pillar_id, sub_pillar)
