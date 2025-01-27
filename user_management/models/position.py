"""This module contains the position module"""
from django.db import models


class Position(models.Model):
    """Position module"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'position'

    @classmethod
    def from_to(cls, instance):
        """
        Creates a Position instance from a PositionTO instance without saving it.

        Args:
            instance (PositionTO): Transfer Object containing the Position data.

        Returns:
            Position: An instance of the Position model.
        """
        from user_management.contract.to.position_to import PositionTO
        if instance is None:
            return None

        if not isinstance(instance, PositionTO):
            raise ValueError("The argument must be an instance of PositionTO")

        # Create the Position instance without saving
        position_instance = cls(
            id=instance.id if instance.id else None,
            name=instance.name,
        )

        return position_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
