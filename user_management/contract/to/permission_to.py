'''This module contains the Permission Transfer Object'''
from dataclasses import asdict, dataclass
from typing import Dict

from common.contract.to.base_to import BaseTO
from user_management.models import Permission


@dataclass
class PermissionTO(BaseTO):
    id: int
    name: str
    type: str
    alias:str

    @classmethod
    def from_model(cls, instance: Permission):
        """Transforms Permission instance into a PermissionTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            type=instance.type,
            alias=instance.alias,
        )

    def to_dict(self) -> Dict:
        return asdict(self)
