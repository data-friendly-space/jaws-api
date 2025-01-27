"""This module contains the analysis repository"""
from abc import abstractmethod

from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.contract.to.analysis_to import AnalysisTO
from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.entry_to import EntryTO
from analysis.contract.to.issue_to import IssueTO
from analysis.contract.to.pillar_to import PillarTO
from analysis.contract.to.sub_pillar_to import SubPillarTO
from analysis.models import AdministrativeDivision
from analysis.models.analysis import Analysis
from common.helpers.query_options import QueryOptions
from common.repository.base_repository import BaseRepository


class AnalysisRepository(BaseRepository):
    """Analysis repository"""


    @abstractmethod
    def get_or_create_entry(self, entry_to: EntryTO) -> EntryTO:
        """Get or create entry"""

    @abstractmethod
    def create_issue(self, issue_to: IssueTO) -> IssueTO:
        """Create Issue"""

    @abstractmethod
    def get_issues(self, analysis_id: int) -> list[IssueTO]:
        """Get Issues"""

    @abstractmethod
    def create(self, data, disaggregations, sectors):
        """Create Analysis"""

    @abstractmethod
    def get_or_create_analysis_framework(self, name):
        """Get or Create Analysis Framework"""

    @abstractmethod
    def get_or_create_pillar(self, name) -> PillarTO:
        """Get or Create Pillar"""

    @abstractmethod
    def get_or_create_sub_pillar(self, name) -> SubPillarTO:
        """Get or Create Sub pillar"""

    @abstractmethod
    def add_sub_pillar_to_pillar(self, pillar_id: int, sub_pillar_to: SubPillarTO) -> PillarTO:
        """add pillar to sub pillar"""

    @abstractmethod
    def add_pillar_to_analysis_framework(self, analysis_framework_id: int,
                                         pillar_to: PillarTO) -> AnalysisFrameworkTO:
        """add pillars to analysis_framework"""

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

    @abstractmethod
    def get_subpillar(self, subpillar_id: int) -> SubPillarTO:
        """Retrieve a subpillar by id
        
        Keyword arguments:
        subpillar_id -- the id of the subpillar
        Return: The subpillar as dto
        """

    @abstractmethod
    def update(self, obj_id, data, sectors, disaggregations):
        """update analysis"""
