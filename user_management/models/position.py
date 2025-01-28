"""This module contains the position module"""
from django.db import models, transaction

from common.models import BaseModel


class Position(models.Model, BaseModel):
    """Position module"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'position'

    @classmethod
    def from_to(cls, position_to):
        """
        Creates or updates a Position instance from a PositionTO instance.

        Args:
            position_to (PositionTO): Transfer Object containing the Position data.

        Returns:
            Position: An instance of the Position model.
        """
        from user_management.contract.to.position_to import PositionTO

        if position_to is None:
            return None

        if not isinstance(position_to, PositionTO):
            raise ValueError("The argument must be an instance of PositionTO")

        # Build the defaults dictionary
        defaults = {
            "id": position_to.id if position_to.id else None,
            "name": position_to.name,
        }

        # Filter out None values to avoid overwriting existing data
        defaults = {key: value for key, value in defaults.items() if value is not None}

        with transaction.atomic():
            # Update or create the Position instance
            position_instance, created = cls.objects.update_or_create(
                id=position_to.id,  # Match by ID if provided
                defaults=defaults,
            )

        return position_instance
