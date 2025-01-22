"""This module contains the disaggregation Transfer Object"""
from dataclasses import dataclass

from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.entry_to import EntryTO
from analysis.models.issue import Issue
from charts.contract.dto.chart_to import ChartTO
from common.contract.to.base_to import BaseTO


@dataclass
class IssueTO(BaseTO):
    """Issue DTO"""
    id: int
    name: str
    description: str
    informationGaps: str
    assumptions: str
    disaggregation: DisaggregationTO
    entries: list[EntryTO]
    charts: list[ChartTO]

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
        )
