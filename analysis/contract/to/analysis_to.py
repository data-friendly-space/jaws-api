'''This module contains the Analysis Transfer Object'''
from _pydatetime import date
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.contract.to.analysis_question_to import AnalysisQuestionTO
from analysis.contract.to.analysis_step_to import AnalysisStepTO
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
    sectors: Optional[list[SectorTO]]
    workspace: dict
    lastChange: datetime | None
    disaggregations: Optional[dict] = None
    startDate: date | None = None
    creator: Optional[str] = None
    locations: Optional[list[AdministrativeDivisionTO]] = None
    analysisSteps: Optional[list[AnalysisStepTO]] = None
    analysisQuestions: Optional[list[AnalysisQuestionTO]] = None
    analysisFramework: Optional[AnalysisFrameworkTO] = None

    @classmethod
    def from_model(cls, instance: Analysis):
        """Transforms Analysis instance into a AnalysisDTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            title=instance.title,
            objectives=instance.objectives,
            creator=instance.creator.email,
            workspace={
                "id": instance.workspace.id,
                "title": instance.workspace.title
            },
            startDate=instance.start_date,
            endDate=instance.end_date,
            lastChange=instance.last_change,
            createdOn=instance.created_on,
            disaggregations=DisaggregationTO.from_models(instance.disaggregations.all()),
            sectors=SectorTO.from_models(instance.sectors.all()),
            locations=AdministrativeDivisionTO.from_models(
                instance.locations.all(),
                True),
            analysisSteps=AnalysisStepTO.from_models(instance.analysis_steps.all()),
            analysisFramework=AnalysisFrameworkTO.from_model(instance.analysis_framework),
            analysisQuestions=AnalysisQuestionTO.from_models(instance.analysis_questions.all()),

        )

    def to_dict(self):
        if self.locations:
            self.locations = [location.to_dict() for location in self.locations]
        return asdict(self)
