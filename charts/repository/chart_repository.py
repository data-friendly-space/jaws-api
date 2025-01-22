"""Contains the abstract chart repository"""

from abc import abstractmethod
from typing import List, Optional

from charts.contract.dto.chart_to import ChartTO


class ChartRepository:
    """Abstract repository"""


    @abstractmethod
    def get_chart_by_id(self, chart_id: int) -> ChartTO:
        """Gets a chart by its ID"""
        
    @abstractmethod
    def save(
        self,
        user,
        chart_type: str,
        dataset_id: str,
        analysis_id: int,
        name: str,
        x_col: str,
        subpillar_id: int,
        y_cols: List[str],
        title: Optional[str],
        x_label: Optional[str],
        y_label: Optional[str],
    ) -> ChartTO:
        """Save the chart configuration in the database
        
        Keyword arguments:
        user -- the creator of the chart
        chart_type -- the type of the chart. Should be on the Chart.Type choices
        dataset_id -- the id of the dataset
        analysis_id -- the id of the analysis where the chart belongs
        name -- The name to be displayed
        title -- The title of the chart on top of it
        x_col -- The column of the dataset to be used as x axis
        subpillar -- The subpillar that the chart is aiming to
        y_cols -- the columns of the dataset to be used as y axis
        x_label -- The label of the x axis
        y_label -- the label of the y axis
        Return: The chart dto
        """

    @abstractmethod
    def get(self, analysis_id: int, subpillar_ids: List[int]) -> List[ChartTO]:
        """Retrieve the charts that belong to the analysis filtered by subpillars
        
        Keyword arguments:
        analysis_id -- the id of the analysis
        subpillar_ids -- the ids of each subpillar to use as a filter
        Return: a list of charts to
        """
