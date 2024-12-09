'''This module contains the Workspace Transfer Object'''
import datetime
from typing import Optional

from analysis.contract.dto.analysis_to import AnalysisTO
from user_management.contract.to.user_to import UserTO
from user_management.models import Workspace


class WorkspaceTO:
    def __init__(
            self,
            id: int,
            title: str,
            creation_date: datetime,
            last_access_date: datetime,
            facilitator: Optional[dict],
            country: str,
            analysis: Optional[dict] = None

    ):
        self.id = id
        self.title = title
        self.creation_date = creation_date
        self.last_access_date = last_access_date
        self.facilitator = facilitator
        self.country = country
        self.analysis = analysis

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
