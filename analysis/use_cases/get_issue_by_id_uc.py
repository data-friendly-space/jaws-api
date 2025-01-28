from analysis.contract.to.issue_to import IssueTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetIssueByIdUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetIssueByIdUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetIssueByIdUC._instance = self

    @staticmethod
    def get_instance():
        if GetIssueByIdUC._instance is None:
            GetIssueByIdUC()
        return GetIssueByIdUC._instance

    def exec(self, repository: AnalysisRepository, issue_id: int) -> IssueTO:
        return repository.get_issue_by_id(issue_id)
