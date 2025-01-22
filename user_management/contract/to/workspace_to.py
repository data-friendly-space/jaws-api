'''This module contains the Workspace Transfer Object'''
import datetime
from dataclasses import dataclass
from typing import Optional

from common.contract.to.base_to import BaseTO
from user_management.contract.to.user_to import UserTO
from user_management.models import Workspace


@dataclass
class WorkspaceLiteTO(BaseTO):
    id: str
    title: str

    @classmethod
    def from_model(cls, instance: Workspace):
        """Transforms Workspace instance into a WorkspaceTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            title=instance.title,
        )


@dataclass
class WorkspaceTO(WorkspaceLiteTO, BaseTO):
    creationDate: datetime
    lastAccessDate: datetime
    facilitator: UserTO
    country: str
    creator: UserTO
    analyses: Optional[list['AnalysisTO']]

    @classmethod
    def from_model(cls, instance: Workspace):
        """Transforms Workspace instance into a WorkspaceTO representation."""
        from analysis.contract.to.analysis_to import AnalysisTO
        if instance is None:  # Handle case when instance is None
            return None

        # Reuse WorkspaceLiteTO logic for shared fields
        lite_data = WorkspaceLiteTO.from_model(instance)

        # Add fields specific to WorkspaceTO
        return cls(
            id=lite_data.id,
            title=lite_data.title,
            creationDate=instance.creation_date,
            lastAccessDate=instance.last_access_date,
            facilitator=UserTO.from_model(instance.facilitator),
            creator=UserTO.from_model(instance.creator),
            country=instance.country,
            analyses=AnalysisTO.from_models(instance.analyses.all()),
        )
