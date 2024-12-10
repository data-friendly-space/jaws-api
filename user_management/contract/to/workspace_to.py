'''This module contains the Workspace Transfer Object'''
import datetime
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from analysis.contract.to.analysis_to import AnalysisTO
from user_management.contract.to.user_to import UserTO
from user_management.models import Workspace


@dataclass
class WorkspaceTO:
    id: int
    title: str
    creation_date: datetime
    last_access_date: datetime
    facilitator: Optional[dict]
    country: str
    analysis: Optional[dict] = None

    @classmethod
    def from_model(cls, instance: Workspace):
        """Transforms Workspace instance into a WorkspaceTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            title=instance.title,
            creation_date=instance.creation_date,
            last_access_date=instance.last_access_date,
            facilitator=UserTO.from_model(instance.facilitator),
            country=instance.country,
            analysis=AnalysisTO.from_models(instance.analysis.all())
        )

    @classmethod
    def from_models(self, users):
        """
        Transform a list of Workspace model instances into a list of WorkspaceTO instances.
        """
        return [self.from_model(user) for user in users]

    def to_dict(self) -> Dict:
        return asdict(self)
