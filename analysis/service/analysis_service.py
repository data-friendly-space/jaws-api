from abc import abstractmethod

from analysis.use_cases.create_analysis_uc import CreateAnalysisUC
from analysis.use_cases.get_analysis_by_id_uc import GetAnalysisByIdUC
from analysis.use_cases.get_analysis_uc import GetAnalysisUC
from analysis.use_cases.put_analysis_scope_uc import PutAnalysisScopeUC
from common.service.base_service import BaseService


class AnalysisService(BaseService):

    def __init__(self):
        self.create_analysis_uc = CreateAnalysisUC.get_instance()
        self.put_analysis_scope_uc = PutAnalysisScopeUC.get_instance()
        self.get_analysis_uc = GetAnalysisUC.get_instance()
        self.get_analysis_by_id_uc = GetAnalysisByIdUC.get_instance()

    @abstractmethod
    def put_analysis_scope(self):
        pass

    @abstractmethod
    def get_analysis(self):
        pass

    @abstractmethod
    def create_analysis(self):
        pass
