"""Contains the abstract class of chart service"""

from abc import abstractmethod
from common.service.base_service import BaseService


class ChartService(BaseService):
    """Service for charts management"""

    @abstractmethod
    def save_chart(self, user, config: dict):
        """Save a chart"""
