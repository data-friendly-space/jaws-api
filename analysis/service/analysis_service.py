"""Contains the abstract class of analysis service"""

from abc import abstractmethod

from common.service.base_service import BaseService


class AnalysisService(BaseService):
    """Definition of the analysis service"""

    @abstractmethod
    def put_analysis_scope(self, analysis, analysis_id, user_id):
        """
        Update an analysis scope with the given scope and the analysis id.
        Validate that the user has the required permissions
        """

    @abstractmethod
    def get_analysis(self):
        """Retrieve all the analysis that a user can access"""

    @abstractmethod
    def get_analysis_by_id(self, analysis_id):
        """Retrieve an analysis based on a specific id"""

    @abstractmethod
    def create_analysis(self, analysis, creator_id):
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
