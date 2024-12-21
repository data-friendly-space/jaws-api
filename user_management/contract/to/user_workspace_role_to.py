'''This module contains the Workspace Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO
from user_management.contract.to.role_to import RoleTO
from user_management.contract.to.workspace_to import WorkspaceTO
from user_management.models import UserWorkspaceRole


@dataclass
class UserWorkspaceRoleTO(BaseTO):
    workspace: WorkspaceTO
    role: RoleTO

    @classmethod
    def from_model(cls, instance: UserWorkspaceRole):
        """Transforms UserWorkspaceRole instance into a UserWorkspaceRoleTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            workspace=WorkspaceTO.from_model(instance.workspace),
            role=RoleTO.from_model(instance.role),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
