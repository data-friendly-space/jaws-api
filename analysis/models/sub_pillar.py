"""This module contains the sub_pillar model"""

from django.db import models, transaction

from common.models import BaseModel


class SubPillar(models.Model, BaseModel):
    """Sector model"""
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=200, null=True)

    class Meta:
        """Table's metadata"""
        db_table = 'sub_pillar'

    @classmethod
    def from_to(cls, sub_pillar_to):
        """
        Creates or updates a SubPillar instance from a SubPillarTO instance.

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

        # Build the defaults dictionary
        defaults = {
            "name": sub_pillar_to.name,
        }

        # Filter out None values to avoid overwriting existing data
        defaults = {key: value for key, value in defaults.items() if value is not None}

        with transaction.atomic():
            # Update or create the SubPillar instance
            sub_pillar_instance, created = cls.objects.update_or_create(
                id=sub_pillar_to.id,  # Match by ID if provided
                defaults=defaults,
            )

        return sub_pillar_instance
