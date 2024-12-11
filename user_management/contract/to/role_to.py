"""This module contains the Role Transfer Object"""
from dataclasses import dataclass, asdict

from common.contract.to.base_to import BaseTO
from user_management.contract.to.permission_to import PermissionTO
from user_management.models import Role
from typing import Optional, Dict


@dataclass
class RoleTO(BaseTO):
    id: int
    role: str
    permissions: list[PermissionTO | None]

    @classmethod
    def from_model(cls, instance: Role) -> 'RoleTO | None':
        """Transforms Role instance into a RoleTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            role=instance.role,
            permissions=PermissionTO.from_models(instance.permissions.all())
        )

    def to_dict(self) -> Dict:
        return asdict(self)
