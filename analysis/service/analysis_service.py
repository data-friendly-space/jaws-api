"""Contains the abstract class of analysis service"""

from abc import abstractmethod

from analysis.use_cases.add_location_uc import AddLocationUC
from analysis.use_cases.create_analysis_uc import CreateAnalysisUC
from analysis.use_cases.get_administrative_divisions_uc import (
    GetAdministrativeDivisionByIdUC,
    GetAdministrativeDivisionsUC,
)
from analysis.use_cases.get_analysis_by_id_uc import GetAnalysisByIdUC
from analysis.use_cases.get_analysis_uc import GetAnalysisUC
from analysis.use_cases.put_analysis_scope_uc import PutAnalysisScopeUC
from analysis.use_cases.remove_location_uc import RemoveLocationUC
from common.service.base_service import BaseService


class AnalysisService(BaseService):
    """Definition of the analysis service"""

    def __init__(self):
        self.create_analysis_uc = CreateAnalysisUC.get_instance()
        self.put_analysis_scope_uc = PutAnalysisScopeUC.get_instance()
        self.get_analysis_uc = GetAnalysisUC.get_instance()
        self.get_analysis_by_id_uc = GetAnalysisByIdUC.get_instance()
        self.get_administrative_divisions_uc = (
            GetAdministrativeDivisionsUC.get_instance()
        )
        self.get_administrative_division_by_id_uc = (
            GetAdministrativeDivisionByIdUC.get_instance()
        )
        self.add_location_uc = AddLocationUC.get_instance()
        self.remove_location_uc = RemoveLocationUC.get_instance()

    @abstractmethod
    def put_analysis_scope(self, scope, analysis_id):
        """Update an analysis scope with the given scope and the analysis id"""

    @abstractmethod
    def get_analysis(self):
        """Retrieve all the analysis that a user can access"""

    @abstractmethod
    def get_analysis_by_id(self, analysis_id):
        """Retrieve an analysis based on a specific id"""

    @abstractmethod
    def create_analysis(self, scope):
        """Create a new analysis with the given scope"""

    @abstractmethod
    def get_administrative_divisions(self, parent_p_code):
        """
        Retrieves all the administrative divisions within the parent code.
        If the parent code is null, retireves all the level 0 administrative divisions
        """

    @abstractmethod
    def add_location(self, analysis_id, p_code):
        """
        Add a new location if it is not present yet into a specific analysis
        """

    @abstractmethod
    def remove_location(self, analysis_id, p_code):
        """
        Remove an existing location from an analysis
        """
