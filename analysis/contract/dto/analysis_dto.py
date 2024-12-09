"""This module contains the analysis DTO"""
from typing import Optional

from analysis.contract.dto.administrative_division_dto import AdministrativeDivisionTO
from analysis.contract.dto.disaggregation_dto import DisaggregationTO
from analysis.contract.dto.sector_dto import SectorTO
from analysis.models.analysis import Analysis


class AnalysisTO:
    """Analysis Data Transfer Object"""
    def __init__(
            self,
            id: str,
            title: str,
            objetives: str,
            created_on: str,
            end_date: str,
            sectors: Optional[dict],
            workspace_id: Optional[dict],
            last_change: Optional[dict],
            disaggregations: Optional[dict] = None,
            start_date: Optional[str] = None,
            creator: Optional[str] = None,
            locations: Optional[str] = None
    ):
        self.id = id
        self.objetives = objetives
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
            objetives=instance.objetives,
            creator=instance.creator,
            workspace_id=instance.workspace_id,
            start_date=instance.start_date,
            end_date=instance.end_date,
            last_change=instance.last_change,
            created_on=instance.created_on,
            disaggregations=DisaggregationTO.from_models(instance.disaggregations),
            sectors=SectorTO.from_models(instance.sectors),
            locations=AdministrativeDivisionTO.from_models(instance.locations, include_hierarchy=True)
        )

    @classmethod
    def from_models(cls, analyses):
        """
        Transform a list of Analysis model instances into a list of AnalysisDTO instances.
        """
        return [cls.from_model(analysis) for analysis in analyses]
