'''This module contains the Pillar Transfer Object'''
from dataclasses import dataclass
from typing import Optional

from analysis.contract.to.sub_pillar_to import SubPillarTO
from analysis.models.pillar import Pillar
from common.contract.to.base_to import BaseTO


@dataclass
class PillarTO(BaseTO):
    '''Pillar Transfer Object'''
    id: int
    name: str
    alias: Optional[str]
    subPillars:list[SubPillarTO]
    model_class = Pillar


    @classmethod
    def from_model(cls, instance: Pillar):
        """Transforms Pillar instance into a PillarTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            alias=instance.alias,
            subPillars=SubPillarTO.from_models(instance.sub_pillars.all())
        )