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
    model_class = SubPillar

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

    def to_model(self) -> SubPillar:
        """Transforms SubPillarTO instance into a SubPillar model instance."""
        # Create or update the SubPillar instance
        sub_pillar, created = SubPillar.objects.get_or_create(
            id=self.id,
            defaults={
                'name': self.name,
                'alias': self.alias
            }
        )
        if not created:
            # Update the existing SubPillar instance
            sub_pillar.name = self.name
            sub_pillar.alias = self.alias
            sub_pillar.save()

        return sub_pillar