from analysis.contract.repository.analysis_repository import AnalysisRepository
from app.core.use_case.base_use_case import BaseUseCase


class PutAnalysisScopeUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if PutAnalysisScopeUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PutAnalysisScopeUC._instance = self

    @staticmethod
    def get_instance():
        if PutAnalysisScopeUC._instance is None:
            PutAnalysisScopeUC()
        return PutAnalysisScopeUC._instance

    def exec(self, repository: AnalysisRepository, data, analysis_id, sectors, disaggregations):
        return repository.update(obj_id=analysis_id, sectors=sectors, disaggregations=disaggregations, data=data)
