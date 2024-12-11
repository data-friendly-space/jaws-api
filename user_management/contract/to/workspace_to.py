'''This module contains the Workspace Transfer Object'''
import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from analysis.contract.to.analysis_to import AnalysisTO
from common.contract.to.base_to import BaseTO
from user_management.contract.to.user_to import UserTO
from user_management.models import Workspace


@dataclass
class WorkspaceTO(BaseTO):
    id: str
    title: str
    creationDate: datetime
    lastAccessDate: datetime
    facilitator: UserTO
    country: str
    analyses: Optional[list[AnalysisTO]]

    @classmethod
    def from_model(cls, instance: Workspace):
        """Transforms Workspace instance into a WorkspaceTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            title=instance.title,
            creationDate=instance.creation_date,
            lastAccessDate=instance.last_access_date,
            facilitator=UserTO.from_model(instance.facilitator),
            country=instance.country,
            analyses=AnalysisTO.from_models(instance.analyses.all())
        )

    def to_dict(self) -> Dict:
        return asdict(self)
