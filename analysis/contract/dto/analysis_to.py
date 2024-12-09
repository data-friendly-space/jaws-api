'''This module contains the Analysis Transfer Object'''
from _pydatetime import date
from datetime import datetime
from typing import Optional

from analysis.contract.dto.disaggregation_to import DisaggregationTO
from analysis.contract.dto.sector_to import SectorTO
from analysis.models.analysis import Analysis


class AnalysisTO:
    '''Analysis Data Transfer Object'''

    def __init__(
            self,
            id: str,
            title: str,
            objectives: str,
            sectors: Optional[dict],
            workspace_id: str,
            last_change: Optional[datetime] = None,
            end_date: Optional[date] = None,
            created_on: Optional[datetime] = None,
            disaggregations: Optional[dict] = None,
            start_date: Optional[date] = None,
            creator: Optional[str] = None
    ):
        self.id = id
        self.objectives = objectives
        self.title = title
        self.created_on = created_on
        self.start_date = start_date
        self.end_date = end_date
        self.disaggregations = disaggregations
        self.sectors = sectors
        self.workspace_id = workspace_id
        self.last_change = last_change
        self.creator = creator

    @classmethod
    def from_model(cls, instance: Analysis):
        """Transforms Analysis instance into a AnalysisTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            title=instance.title,
            objectives=instance.objectives,
            creator=instance.creator,
            workspace_id=instance.workspace_id,
            start_date=instance.start_date,
            end_date=instance.end_date,
            last_change=instance.last_change,
            created_on=instance.created_on,
            disaggregations=DisaggregationTO.from_models(instance.disaggregations),
            sectors=SectorTO.from_models(instance.sectors),
        )

    @classmethod
    def from_models(cls, analyses):
        """
        Transform a list of Analysis model instances into a list of AnalysisTO instances.
        """

        return [cls.from_model(analysis) for analysis in analyses]
