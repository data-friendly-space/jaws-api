from analysis.contract.to.issue_to import IssueTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetIssuesByAnalysisIdUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetIssuesByAnalysisIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetIssuesByAnalysisIdUC._instance = self

    @staticmethod
    def get_instance():
        if GetIssuesByAnalysisIdUC._instance is None:
            GetIssuesByAnalysisIdUC()
        return GetIssuesByAnalysisIdUC._instance

    def exec(self, repository: AnalysisRepository, analysis_id: int) -> list[IssueTO]:
        return repository.get_issues(analysis_id)
