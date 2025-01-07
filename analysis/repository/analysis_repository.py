"""This module contains the analysis repository"""
from abc import abstractmethod

from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.contract.to.analysis_to import AnalysisTO
from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.models import AdministrativeDivision
from analysis.models.analysis import Analysis
from common.helpers.query_options import QueryOptions
from common.repository.base_repository import BaseRepository


class AnalysisRepository(BaseRepository):
    """Analysis repository"""

    @abstractmethod
    def invite_user_to_analysis(self, user_id: str, analysis_id: str, role_id: str):
        """Invite user to analysis"""

    @abstractmethod
    def get_all_sectors(self, **kwargs):
        """Get all sectors"""

    @abstractmethod
    def get_administrative_divisions(self, parent_p_code):
        """
        Retrieves every administrative division within the parent p_code.
        If parent p_code is None, retrieve all the level 0 administrative divisions
        """

    @abstractmethod
    def get_administrative_division(self, p_code) -> AdministrativeDivisionTO:
        """Retrieves a specific administrative division by p_code"""

    @abstractmethod
    def add_location(self, analysis_to: AnalysisTO, administrative_division_to: AdministrativeDivisionTO):
        """Add a new administrative division into a analysis"""

    @abstractmethod
    def remove_location(self, analysis: Analysis, administrative_division: AdministrativeDivision):
        """Add a new administrative division into a analysis"""

    @abstractmethod
    def get_steps(self):
        """Return the analysis steps"""

    @abstractmethod
    def get_steps_by_ids(self, ids):
        """Return analysis steps based on a list of ids"""

    @abstractmethod
    def update_analysis_questions(self, analysis_id: int, content: str) -> AnalysisTO:
        """Assign or update analysis questions"""

    @abstractmethod
    def assign_or_update_framework_to_analysis(self, analysis_id: int, framework_id: int) -> AnalysisTO:
        """
        Update the analysis_framework field for a specific Analysis instance.
        :param analysis_id: ID of the Analysis to update.
        :param framework_id: ID of the AnalysisFramework to set.
        :return: Number of rows updated.
        """

    @abstractmethod
    def get_all_disaggregations(self, query_options: QueryOptions, **kwargs) -> list[DisaggregationTO]:
        """Return all disaggregations"""
