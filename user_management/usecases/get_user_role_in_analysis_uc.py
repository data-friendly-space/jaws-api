"""This module contains the use case for getting the user's role within an analysis"""
from user_management.contract.repository.role_repository import RoleRepository


class GetUserRoleInAnalysisUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if GetUserRoleInAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUserRoleInAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetUserRoleInAnalysisUC._instance is None:
            GetUserRoleInAnalysisUC()
        return GetUserRoleInAnalysisUC._instance

    def exec(self, repository: RoleRepository, user_id, analysis_id):
        """Execute the use case"""
        return repository.get_user_role_in_analysis(user_id, analysis_id)
