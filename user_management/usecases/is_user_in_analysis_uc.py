"""This module contains use case for knowing if a user belongs to an analysis"""
from common.use_case.base_use_case import BaseUseCase
from user_management.contract.repository.user_repository import UserRepository


class IsUserInAnalysisUC(BaseUseCase):
    """Class for verifying if an user belongs to an analysis"""
    _instance = None

    def __init__(self):
        if IsUserInAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            IsUserInAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        """Returns an instance of the class"""
        if IsUserInAnalysisUC._instance is None:
            IsUserInAnalysisUC()
        return IsUserInAnalysisUC._instance

    def exec(self, repository: UserRepository, user_id: str, analysis_id: int):
        """Execute de use case"""
        return repository.is_user_in_analysis(user_id, analysis_id)
