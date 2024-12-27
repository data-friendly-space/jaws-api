'''This module contains the Dataset Transfer Object'''
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict

from common.contract.to.base_to import BaseTO
from file_management.models.dataset import Dataset
from user_management.contract.to.user_to import UserTO


@dataclass
class DatasetTO(BaseTO):
    """Contains the fields for a dataset"""
    id: str | None
    uploadedBy: UserTO | None
    createdOn: datetime | None
    url: str | None
    filename: str | None


    @classmethod
    def from_model(cls, instance: Dataset) -> 'DatasetTO | None':
        """Transforms the Dataset model into DatasetTO"""
        if not instance:
            return None
        return cls(
            uploadedBy=instance.uploaded_by,
            createdOn=instance.created_on,
            id=instance.id,
            filename=instance.filename,
            url=instance.url
        )

    def to_dict(self) -> Dict:
        return asdict(self)
