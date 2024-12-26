from dataclasses import dataclass

from common.contract.to.base_to import BaseTO
from user_management.models import Organization


@dataclass
class OrganizationTO(BaseTO):
    id: int
    name: str

    @classmethod
    def from_model(cls, instance: Organization):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Organization instance into a OrganizationTO representation."""
        return cls(
            id=instance.id,
            name=instance.name,
        )
