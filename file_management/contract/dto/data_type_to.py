'''This module contains the Dataset Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO
from file_management.models.data_type import DataType


@dataclass
class DataTypeTO(BaseTO):
    """Contains the fields for a dataset"""
    id: str | None
    name: str | None


    @classmethod
    def from_model(cls, instance: DataType) -> 'DataTypeTO | None':
        """Transforms the DataType model into DataTypeTO"""
        if not instance:
            return None
        return cls(
            id=instance.id,
            name=instance.name)

    def to_dict(self) -> Dict:
        return asdict(self)
