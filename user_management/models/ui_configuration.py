"""This module contains the ui configuration model"""
from django.db import models


class UiConfiguration(models.Model):
    """Ui configuration module"""
    color = models.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = None

    def __str__(self):
        return "UI Configuration"

    class Meta:
        db_table = 'ui_configuration'

    @classmethod
    def from_to(cls, instance):
        """
        Creates a UiConfiguration instance from a UiConfigurationTO instance without saving it.

        Args:
            instance (UiConfigurationTO): Transfer Object containing the UiConfiguration data.

        Returns:
            UiConfiguration: An instance of the UiConfiguration model.
        """
        from user_management.contract.to.ui_configuration_to import UiConfigurationTO
        if instance is None:
            return None

        if not isinstance(instance, UiConfigurationTO):
            raise ValueError("The argument must be an instance of UiConfigurationTO")

        # Create the UiConfiguration instance without saving
        ui_configuration_instance = cls(
            id=instance.id if instance.id else None,
            color=instance.color,
        )

        return ui_configuration_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
