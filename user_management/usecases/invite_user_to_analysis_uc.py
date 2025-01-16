"""This module contains the get users use case"""
from analysis.repository.analysis_repository import AnalysisRepository


class InviteUserToAnalysisUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if InviteUserToAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            InviteUserToAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if InviteUserToAnalysisUC._instance is None:
            InviteUserToAnalysisUC()
        return InviteUserToAnalysisUC._instance

    def exec(self, repository: AnalysisRepository, user_id: str, analysis_id: str, role_id: str):
        """Execute the use case"""
        return repository.invite_user_to_analysis(user_id, analysis_id, role_id)
