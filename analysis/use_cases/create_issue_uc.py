from analysis.contract.to.issue_to import IssueTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class CreateIssueUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if CreateIssueUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateIssueUC._instance = self

    @staticmethod
    def get_instance():
        if CreateIssueUC._instance is None:
            CreateIssueUC()
        return CreateIssueUC._instance

    def exec(self, repository: AnalysisRepository, issue_to: IssueTO) -> IssueTO:
        return repository.create_issue(issue_to)
