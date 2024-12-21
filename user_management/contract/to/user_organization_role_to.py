'''This module contains the Organization Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO
from user_management.contract.to.organization_to import OrganizationTO
from user_management.contract.to.role_to import RoleTO
from user_management.models.user_organization_role import UserOrganizationRole


@dataclass
class UserOrganizationRoleTO(BaseTO):
    organization: OrganizationTO
    role: RoleTO

    @classmethod
    def from_model(cls, instance: UserOrganizationRole):
        """Transforms UserOrganizationRole instance into a UserOrganizationRoleTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            organization=OrganizationTO.from_model(instance.organization),
            role=RoleTO.from_model(instance.role),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
