"""This module contains the Role Transfer Object"""
from dataclasses import dataclass

from common.contract.to.base_to import BaseTO
from user_management.contract.to.permission_to import PermissionTO
from user_management.models import Role
from typing import Optional


@dataclass
class RoleTO(BaseTO):
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
    def from_model(cls, instance: Role) -> 'RoleTO':
        """Transforms Role instance into a RoleTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            role=instance.role,
            permissions=PermissionTO.from_models(instance.permissions.all())
        )
