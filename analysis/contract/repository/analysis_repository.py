"""This module contains the analysis repository"""
from abc import abstractmethod

from common.repository.base_repository import BaseRepository


class AnalysisRepository(BaseRepository):
    """Analysis repository"""

    @abstractmethod
    def invite_user_to_analysis(self, user_id: str, analysis_id: str, role_id: str):
        """Invite user to analysis"""
