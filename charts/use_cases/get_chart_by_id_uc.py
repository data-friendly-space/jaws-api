"""This module contains the get charts use case"""
from typing import List
from charts.contract.dto.chart_to import ChartTO
from charts.repository.chart_repository import ChartRepository
from common.exceptions.exceptions import InternalServerErrorException
from common.use_case.base_use_case import BaseUseCase


class GetChartByIdUC(BaseUseCase):
    """Get the charts of an analysis filtered by subpillars"""
    _instance = None

    def __init__(self):
        if GetChartByIdUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            GetChartByIdUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetChartByIdUC._instance is None:
            GetChartByIdUC()
        return GetChartByIdUC._instance

    def exec(self, repository: ChartRepository, chart_id: int) -> ChartTO:
        """Execute the use case"""
        return repository.get_chart_by_id(chart_id)
