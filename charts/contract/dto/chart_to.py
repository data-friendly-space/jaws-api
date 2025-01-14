'''This module contains the Chart TO'''
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from charts.models.chart import Chart
from common.contract.to.base_to import BaseTO
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.dto.dataset_to import DatasetTO


@dataclass
class ChartTO(BaseTO):
    """Contains the fields for chart"""
    dataset: DatasetTO
    name: str
    type: str
    xCol: ColumnConfigurationTO
    yCols: List[ColumnConfigurationTO]
    xLabel: Optional[str]
    yLabel: Optional[str]
    title: Optional[str]

    @classmethod
    def from_model(cls, instance: Chart) -> 'ChartTO | None':
        """Transforms the chart model to chart to"""
        if not instance:
            return None
        return cls(
            dataset=DatasetTO.from_model(instance.dataset),
            type=instance.type,
            name=instance.name,
            title=instance.title,
            xLabel=instance.x_label,
            yLabel=instance.y_label,
            xCol=ColumnConfigurationTO.from_model(instance.x_col),
            yCols=ColumnConfigurationTO.from_models(instance.y_cols.all()),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
