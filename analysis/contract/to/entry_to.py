"""This module contains the disaggregation Transfer Object"""
import datetime
from dataclasses import dataclass
from typing import Optional

from analysis.contract.to.sub_pillar_to import SubPillarTO
from analysis.models.entry import Entry
from common.contract.to.base_to import BaseTO


@dataclass
class EntryTO(BaseTO):
    """Entry TO"""
    id: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    createdBy: str | None = None
    fragment: str | None = None
    source: str | None = None
    tag: Optional[SubPillarTO]  = None

    @classmethod
    def from_model(cls, instance: Entry):
        """Transforms Entry instance into a Entry TO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            createdAt=instance.created_at,
            updatedAt=instance.updated_at,
            createdBy=instance.created_by,
            fragment=instance.fragment,
            source=instance.source,
            tag=SubPillarTO.from_model(instance.tag)
        )
