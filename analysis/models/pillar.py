"""This module contains the pillar model"""
from django.db import models

from analysis.models.sub_pillar import SubPillar


class Pillar(models.Model):
    """Sector model"""
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=200, null=True)
    sub_pillars = models.ManyToManyField(SubPillar)

    class Meta:
        """Table's metadata"""
        db_table = 'pillar'

    @classmethod
    def from_to(cls, pillar_to):
        """
        Creates an Pillar instance from an PillarTO instance without saving it.

        Args:
            pillar_to (PillarTO): Transfer Object containing the Pillar data.

        Returns:
            Pillar: An instance of the Pillar model.
        """
        from analysis.contract.to.pillar_to import PillarTO
        if not isinstance(pillar_to, PillarTO):
            raise ValueError("The argument must be an instance of PillarTO")

        # Create the Pillar instance without saving
        pillar_instance = cls(
            id=pillar_to.id,  # Include only if IDs are passed in the TO
            name=pillar_to.name,
            sub_pillars=SubPillar.from_tos(pillar_to.subPillars)
        )

        return pillar_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]