"""This module contains the disaggregation Transfer Object"""
from dataclasses import dataclass

from analysis.models.entry import Entry
from common.contract.to.base_to import BaseTO


@dataclass
class EntryTO(BaseTO):
    """Entry TO"""
    id: int

    @classmethod
    def from_model(cls, instance: Entry):
        """Transforms Entry instance into a Entry TO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
        )

