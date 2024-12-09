'''This module contains the Permission Transfer Object'''
from user_management.models import Permission


class PermissionTO:
    def __init__(
            self,
            id: int,
            name: str,
            type: str
    ):
        self.id = id
        self.name = name
        self.type = type

    @classmethod
    def from_model(cls, instance: Permission):
        """Transforms Permission instance into a PermissionTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            type=instance.type
        )

    @classmethod
    def from_models(cls, permissions):
        """
        Transform a list of Permission model instances into a list of PermissionTO instances.
        """
        if permissions is None or permissions.count() <= 0:
            return None
        return [cls.from_model(permission) for permission in permissions]
