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
    uploadedBy: str | None
    sizeBytes: int | None
    createdAt: datetime | None
    updatedAt: datetime | None
    mimeType: str | None
    url: str | None
    filename: str | None
    totalRows: int | None
    totalColumns: int | None
    externalIdentifier: str | None


    @classmethod
    def from_model(cls, instance: Dataset) -> 'DatasetTO | None':
        """Transforms the Dataset model into DatasetTO"""
        if not instance:
            return None
        return cls(
            uploadedBy=instance.uploaded_by.id,
            createdAt=instance.created_at,
            id=instance.id,
            sizeBytes=instance.size_bytes,
            mimeType=instance.mime_type,
            updatedAt=instance.updated_at,
            filename=instance.filename,
            url=instance.url,
            totalRows=instance.total_rows,
            totalColumns=instance.total_columns,
            externalIdentifier=instance.external_identifier
        )

    def to_dict(self) -> Dict:
        return asdict(self)
