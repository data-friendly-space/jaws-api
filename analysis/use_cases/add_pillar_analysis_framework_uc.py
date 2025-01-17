from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.contract.to.pillar_to import PillarTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class AddPillarToAnalysisFrameworkUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if AddPillarToAnalysisFrameworkUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AddPillarToAnalysisFrameworkUC._instance = self

    @staticmethod
    def get_instance():
        if AddPillarToAnalysisFrameworkUC._instance is None:
            AddPillarToAnalysisFrameworkUC()
        return AddPillarToAnalysisFrameworkUC._instance

    def exec(self, repository: AnalysisRepository, analysis_framework_id:int, pillar:PillarTO) -> AnalysisFrameworkTO:
        return repository.add_pillar_to_analysis_framework(analysis_framework_id,pillar)
