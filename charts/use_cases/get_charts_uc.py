"""This module contains the get charts use case"""
from typing import List
from charts.contract.dto.chart_to import ChartTO
from charts.repository.chart_repository import ChartRepository
from common.exceptions.exceptions import InternalServerErrorException
from common.use_case.base_use_case import BaseUseCase


class GetChartsUC(BaseUseCase):
    """Get the charts of an analysis filtered by subpillars"""
    _instance = None

    def __init__(self):
        if GetChartsUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            GetChartsUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetChartsUC._instance is None:
            GetChartsUC()
        return GetChartsUC._instance

    def exec(self, repository: ChartRepository, analysis_id: int, subpillar_ids: List[int]) -> List[ChartTO]:
        """Execute the use case"""
        charts = repository.get(
            analysis_id,
            subpillar_ids
        )
        return charts
