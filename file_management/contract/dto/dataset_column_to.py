'''This module contains the Dataset Column Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO
from file_management.contract.dto.data_type_to import DataTypeTO
from file_management.models.column_configuration import ColumnConfiguration


@dataclass
class DatasetColumnTO(BaseTO):
    """Contains the fields for a dataset"""
    id: str | None 
    originalName: str | None
    originalDataType: DataTypeTO | None


    @classmethod
    def from_model(cls, instance: ColumnConfiguration) -> 'DatasetColumnTO | None':
        """Transforms the Dataset Column model into DatasetColumnTO"""
        if not instance:
            return None
        return cls(
            id=instance.id,
            originalName=instance.original_name,
            originalDataType=DataTypeTO.from_model(instance.original_data_type)
        )

    def to_dict(self) -> Dict:
        return asdict(self)
