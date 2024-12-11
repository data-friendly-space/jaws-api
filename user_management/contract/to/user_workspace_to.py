'''This module contains the Workspace Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO
from user_management.contract.to.role_to import RoleTO
from user_management.contract.to.user_to import UserTO
from user_management.models import UserWorkspaceRole


@dataclass
class UserWorkspaceTO(BaseTO):
    user: UserTO
    workspace_id: str
    role: RoleTO

    @classmethod
    def from_model(cls, instance: UserWorkspaceRole):
        """Transforms Workspace instance into a WorkspaceTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            user=UserTO.from_model(instance.user),
            workspace_id=instance.workspace.id,
            role=RoleTO.from_model(instance.role),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
