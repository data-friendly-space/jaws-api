'''This module contains the Analysis Transfer Object'''
from _pydatetime import date
from datetime import datetime
from typing import Optional

from analysis.contract.to.administrative_division_dto import AdministrativeDivisionTO
from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.sector_to import SectorTO
from analysis.models.analysis import Analysis
from common.contract.to.base_to import BaseTO


class AnalysisTO(BaseTO):
    '''Analysis Data Transfer Object'''

    def __init__(
            self,
            id: str,
            title: str,
            objectives: str,
            created_on: datetime | None,
            end_date: date | None,
            sectors: Optional[dict],
            workspace_id: str | None,
            last_change: datetime | None,
            disaggregations: Optional[dict] = None,
            start_date: date | None = None,
            creator: Optional[str] = None,
            locations: Optional[str] = None
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
        self.locations = locations

    @classmethod
    def from_model(cls, instance: Analysis):
        """Transforms Analysis instance into a AnalysisDTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            title=instance.title,
            objectives=instance.objectives,
            creator=instance.creator_id,
            workspace_id=instance.workspace_id,
            start_date=instance.start_date,
            end_date=instance.end_date,
            last_change=instance.last_change,
            created_on=instance.created_on,
            disaggregations=DisaggregationTO.from_models(instance.disaggregations),
            sectors=SectorTO.from_models(instance.sectors),
            locations=AdministrativeDivisionTO.from_models(instance.locations, include_hierarchy=True)
        )
