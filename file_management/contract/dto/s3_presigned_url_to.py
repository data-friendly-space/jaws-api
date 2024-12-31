'''This module contains the User Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Dict

from common.contract.to.base_to import BaseTO


@dataclass
class S3PresignedUrlFieldsTO(BaseTO):
    """Contains the fields for a presigned URL"""
    key: str | None = None
    AWSAccessKeyId: str | None = None
    policy: str | None = None
    signature: str | None = None

    @classmethod
    def from_model(cls, instance: dict) -> 'S3PresignedUrlFieldsTO | None':
        """Transforms the response from AWS into a S3PresignedUrlFieldsTO"""
        if not instance:
            return None
        return cls(
            key=instance['key'],
            AWSAccessKeyId=instance['AWSAccessKeyId'],
            policy=instance['policy'],
            signature=instance['signature']
        )
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class S3PresignedUrlTO(BaseTO):
    """Contains the response from AWS"""
    url: str | None = None
    fields: S3PresignedUrlFieldsTO | None = None

    @classmethod
    def from_model(cls, instance: dict) -> 'S3PresignedUrlTO | None':
        """Transforms User instance into a UserTO representation."""
        if instance is None:
            return None
        return cls(
            url=instance['url'],
            fields=S3PresignedUrlFieldsTO.from_model(instance['fields']),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
