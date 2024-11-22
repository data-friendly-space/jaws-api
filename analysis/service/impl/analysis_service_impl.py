from analysis.repository.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.service.analysis_service import AnalysisService
from analysis.use_cases.put_analysis_scope_uc import PutAnalysisScopeUc


class AnalysisServiceImpl(AnalysisService):
    def __init__(self):
        self.put_scope = PutAnalysisScopeUc.get_instance()

    def put_scope(self):
        return self.put_scope.exec(AnalysisRepositoryImpl())
