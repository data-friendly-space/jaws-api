'''This module contains the Analysis Transfer Object'''
from _pydatetime import date
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from analysis.contract.to.administrative_division_dto import AdministrativeDivisionTO
from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.sector_to import SectorTO
from analysis.models.analysis import Analysis
from common.contract.to.base_to import BaseTO


@dataclass
class AnalysisTO(BaseTO):
    '''Analysis Data Transfer Object'''
    id: int
    title: str
    objectives: str
    createdOn: datetime | None
    endDate: date | None
    sectors: Optional[dict]
    workspaceId: str | None
    lastChange: datetime | None
    disaggregations: Optional[dict] = None,
    startDate: date | None = None,
    creator: Optional[str] = None,
    locations: Optional[str] = None

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
            workspaceId=instance.workspace_id,
            startDate=instance.start_date,
            endDate=instance.end_date,
            lastChange=instance.last_change,
            createdOn=instance.created_on,
            disaggregations=DisaggregationTO.from_models(instance.disaggregations),
            sectors=SectorTO.from_models(instance.sectors),
            locations=AdministrativeDivisionTO.from_models(instance.locations, include_hierarchy=True)
        )
