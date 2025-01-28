from analysis.contract.to.issue_to import IssueTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class CreateOrUpdateIssueUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if CreateOrUpdateIssueUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateOrUpdateIssueUC._instance = self

    @staticmethod
    def get_instance():
        if CreateOrUpdateIssueUC._instance is None:
            CreateOrUpdateIssueUC()
        return CreateOrUpdateIssueUC._instance

    def exec(self, repository: AnalysisRepository, issue_to: IssueTO) -> IssueTO:
        return repository.create_or_update_issue(issue_to)
