'''This module contains the Dataset Transfer Object'''
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict

from common.contract.to.base_to import BaseTO
from file_management.contract.dto.data_role_to import DataRoleTO
from file_management.contract.dto.data_type_to import DataTypeTO
from file_management.models.column_configuration import ColumnConfiguration


@dataclass
class ColumnConfigurationTO(BaseTO):
    """Contains the fields for a dataset"""
    id: str | None 
    alias: str | None
    lastChange: datetime | None
    dataType: str | None
    dataRole: str | None
    include: bool | None
    originalName: str | None


    @classmethod
    def from_model(cls, instance: ColumnConfiguration) -> 'ColumnConfigurationTO | None':
        """Transforms the Dataset model into DatasetTO"""
        if not instance:
            return None
        return cls(
            id=instance.id,
            alias=instance.alias,
            lastChange=instance.last_change,
            dataType=DataTypeTO.from_model(instance.data_type),
            dataRole=DataRoleTO.from_model(instance.data_role),
            include=instance.include,
            originalName=instance.column.original_name
        )

    def to_dict(self) -> Dict:
        return asdict(self)
