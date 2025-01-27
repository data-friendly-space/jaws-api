"""This module contains the affiliation model"""
from django.db import models


class Affiliation(models.Model):
    """Affiliation model"""
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, blank=True, null=True)
    background = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'affiliation'

    @classmethod
    def from_to(cls, instance):
        """
        Creates a Affiliation instance from a AffiliationTO instance without saving it.

        Args:
            instance (AffiliationTO): Transfer Object containing the Affiliation data.

        Returns:
            Affiliation: An instance of the Affiliation model.
        """
        from user_management.contract.to.affiliattion_to import AffiliationTO
        if instance is None:
            return None

        if not isinstance(instance, AffiliationTO):
            raise ValueError("The argument must be an instance of AffiliationTO")

        # Create the Affiliation instance without saving
        user_instance = cls(
            id=instance.id if instance.id else None,
            name=instance.name,
            color = instance.color,
            background = instance.background,
        )

        return user_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
