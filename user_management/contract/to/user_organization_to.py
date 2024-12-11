'''This module contains the Organization Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from user_management.contract.to.organization_to import OrganizationTO
from user_management.contract.to.role_to import RoleTO
from user_management.contract.to.user_to import UserTO
from user_management.models.user_organization_role import UserOrganizationRole


@dataclass
class UserOrganizationTO:
    user: UserTO
    organization: OrganizationTO
    role: RoleTO

    @classmethod
    def from_model(cls, instance: UserOrganizationRole):
        """Transforms Organization instance into a OrganizationTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            user=UserTO.from_model(instance.user),
            organization=OrganizationTO.from_model(instance.organization),
            role=RoleTO.from_model(instance.role),
        )

    @classmethod
    def from_models(self, organizations):
        """
        Transform a list of Organization model instances into a list of OrganizationTO instances.
        """
        return [self.from_model(org) for org in organizations]

    def to_dict(self) -> Dict:
        return asdict(self)
