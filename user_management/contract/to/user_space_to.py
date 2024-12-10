'''This module contains the Workspace Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from user_management.contract.to.role_to import RoleTO
from user_management.models import UserWorkspaceRole


@dataclass
class WorkspaceTO:
    id: int
    workspace: int
    role: Optional[dict]

    @classmethod
    def from_model(cls, instance: UserWorkspaceRole):
        """Transforms Workspace instance into a WorkspaceTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            workspace=instance.workspace_id,
            role=RoleTO.from_models(instance.role),
        )

    @classmethod
    def from_models(self, workspaces):
        """
        Transform a list of Workspace model instances into a list of WorkspaceTO instances.
        """
        return [self.from_model(workspace) for workspace in workspaces]

    def to_dict(self) -> Dict:
        return asdict(self)
