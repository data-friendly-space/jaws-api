'''This module contains the Chart TO'''
from dataclasses import dataclass, asdict
import datetime
from typing import Dict, List, Optional

from analysis.contract.to.sub_pillar_to import SubPillarTO
from charts.models.chart import Chart
from common.contract.to.base_to import BaseTO
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.dto.dataset_to import DatasetTO
from user_management.contract.to.user_to import UserTO


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
    subpillar: SubPillarTO
    createdBy: UserTO
    createdOn: datetime

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
            subpillar=SubPillarTO.from_model(instance.subpillar),
            createdBy=UserTO.from_model(instance.created_by),
            createdOn=instance.created_on
        )

    def to_dict(self) -> Dict:
        return asdict(self)
