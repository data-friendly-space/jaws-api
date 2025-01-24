"""This module contains the disaggregation Transfer Object"""
from dataclasses import dataclass, field
from typing import List, Optional

from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.entry_to import EntryTO
from analysis.models.issue import Issue
from charts.contract.dto.chart_to import ChartTO
from common.contract.to.base_to import BaseTO


@dataclass
class IssueTO(BaseTO):
    """Issue DTO"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    informationGaps: str = ""
    assumptions: str = ""
    disaggregation: Optional[DisaggregationTO] = None
    entries: List[EntryTO] = field(default_factory=list)
    charts: List[ChartTO] = field(default_factory=list)
    analysisId: Optional[int] = None

    @classmethod
    def from_model(cls, instance: Issue):
        """Transforms Issue instance into a Issue TO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            informationGaps=instance.information_gaps,
            assumptions=instance.assumptions,
            disaggregation=DisaggregationTO.from_model(instance.disaggregation),
            entries=EntryTO.from_models(instance.entries.all()),
            charts=ChartTO.from_models(instance.charts.all()),
            analysisId=instance.analysis_id
        )
