'''This module contains the Dataset Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO
from file_management.models.data_role import DataRole


@dataclass
class DataRoleTO(BaseTO):
    """Contains the fields for a dataset"""
    id: str | None
    name: str | None


    @classmethod
    def from_model(cls, instance: DataRole) -> 'DataRoleTO | None':
        """Transforms the DataRole model into DataRoleTO"""
        if not instance:
            return None
        return cls(
            id=instance.id,
            name=instance.name)

    def to_dict(self) -> Dict:
        return asdict(self)
