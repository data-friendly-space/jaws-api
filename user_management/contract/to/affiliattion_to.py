from dataclasses import dataclass

from common.contract.to.base_to import BaseTO
from user_management.models import Affiliation


@dataclass
class AffiliationTO(BaseTO):
    id: int
    name: str

    @classmethod
    def from_model(cls, instance: Affiliation):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Affiliation instance into a AffiliationTO representation."""
        return cls(
            id=instance.id,
            name=instance.name,
        )
