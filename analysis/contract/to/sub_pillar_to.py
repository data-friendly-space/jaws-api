'''This module contains the SubPillar Transfer Object'''
from dataclasses import dataclass
from typing import Optional

from analysis.models.sub_pillar import SubPillar
from common.contract.to.base_to import BaseTO


@dataclass
class SubPillarTO(BaseTO):
    '''SubPillar Transfer Object'''
    id: int
    name: str
    alias: Optional[str]


    @classmethod
    def from_model(cls, instance: SubPillar):
        """Transforms SubPillar instance into a SubPillarTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            alias=instance.alias,
        )