"""This module contains the sub_pillar model"""

from django.db import models
from common.models.base_model import BaseModel


class SubPillar(BaseModel):
    """Sector model"""
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=200, null=True)

    class Meta:
        """Table's metadata"""
        db_table = 'sub_pillar'

    @classmethod
    def from_to(cls, sub_pillar_to):
        """
        Creates a SubPillar instance from a SubPillarTO instance without saving it.

        Args:
            sub_pillar_to (SubPillarTO): Transfer Object containing the SubPillar data.

        Returns:
            SubPillar: An instance of the SubPillar model.
        """
        from analysis.contract.to.sub_pillar_to import SubPillarTO

        if sub_pillar_to is None:
            return None

        if not isinstance(sub_pillar_to, SubPillarTO):
            raise ValueError("The argument must be an instance of SubPillarTO")

        # Create the SubPillar instance without saving
        sub_pillar_instance = cls(
            id=sub_pillar_to.id,  # Include only if IDs are passed in the TO
            name=sub_pillar_to.name,
        )
        sub_pillar_instance.save()
        return sub_pillar_instance
