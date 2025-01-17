"""This module contains the save chart use case"""
from charts.repository.chart_repository import ChartRepository
from common.exceptions.exceptions import InternalServerErrorException
from common.use_case.base_use_case import BaseUseCase


class SaveChartUC(BaseUseCase):
    """Save a chart"""
    _instance = None

    def __init__(self):
        if SaveChartUC._instance is not None:
            raise InternalServerErrorException("This class is a singleton!")
        else:
            SaveChartUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if SaveChartUC._instance is None:
            SaveChartUC()
        return SaveChartUC._instance

    def exec(self, repository: ChartRepository, user, chart: dict):
        """Execute the use case"""
        return repository.save(
            user=user,
            chart_type=chart.get("type"),
            title=chart.get("title", None),
            x_label=chart.get("x_label", None),
            x_col=chart.get("x_col"),
            y_label=chart.get("y_label", None),
            y_cols=chart["y_cols"],
            name=chart["name"],
            analysis_id=chart["analysis_id"],
            dataset_id=chart["dataset_id"],
            subpillar_id=chart["subpillar_id"]
        )
