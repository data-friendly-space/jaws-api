"""This module contains the Role Transfer Object"""
from user_management.contract.to.permission_to import PermissionTO
from user_management.models import Role
from typing import Optional


class RoleTO:
    def __init__(
            self,
            id: int,
            role: str,
            permissions=Optional[dict]
    ):
        self.id = id
        self.role = role
        self.permissions = permissions

    @classmethod
    def from_model(cls, instance: Role):
        """Transforms Role instance into a RoleTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            role=instance.role,
            permissions=PermissionTO.from_models(instance.permissions.all())
        )

    @classmethod
    def from_models(self, roles):
        """
        Transform a list of Role model instances into a list of RoleTO instances.
        """
        if roles is None or roles.count() <= 0:
            return None
        return [self.from_model(role) for role in roles]
