"""Contains the abstract class of chart service"""

from abc import abstractmethod
from typing import List
from common.service.base_service import BaseService


class ChartService(BaseService):
    """Service for charts management"""

    @abstractmethod
    def save_chart(self, user, config: dict) -> dict:
        """Save a chart"""

    @abstractmethod
    def get_charts(self, user, analysis_id: int, subpillars: List[int]) -> List[dict]:
        """Get the charts of an analysis
        
        Keyword arguments:
        analysis_id -- The id of the analysis
        subpillars -- the subpillars to use as filter
        Return: A list of charts as dict
        """
