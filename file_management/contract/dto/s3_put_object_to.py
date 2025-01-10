"""Contains the dto for s3 put object"""
from dataclasses import dataclass, asdict
from typing import Dict, Optional

from common.contract.to.base_to import BaseTO
from file_management.models.data_role import DataRole


@dataclass
class S3PutObjectTO(BaseTO):
    """Contains the fields for S3 put object response"""
    Expiration: Optional[str] = None
    ETag: Optional[str] = None
    ChecksumCRC32L: Optional[str] = None
    ChecksumCRC32C: Optional[str] = None
    ChecksumSHA1: Optional[str] = None
    ChecksumSHA256: Optional[str] = None
    ServerSideEncryption: Optional[str] = None
    VersionId: Optional[str] = None
    SSECustomerAlgorithm: Optional[str] = None
    SSECustomerKeyMD5: Optional[str] = None
    SSEKMSKeyId: Optional[str] = None
    SSEKMSEncryptionContext: Optional[str] = None
    BucketKeyEnabled: Optional[bool] = None
    Size: Optional[int] = None
    RequestCharged: Optional[str] = None



    @classmethod
    def from_model(cls, instance: DataRole) -> 'S3PutObjectTO | None':
        """Transforms the DataRole model into DataRoleTO"""
        if not instance:
            return None
        return cls(
            Expiration=instance.get("Expiration"),
            ETag=instance.get("ETag"),
            ChecksumCRC32L=instance.get("ChecksumCRC32L"),
            ChecksumCRC32C=instance.get("ChecksumCRC32C"),
            ChecksumSHA1=instance.get("ChecksumSHA1"),
            ChecksumSHA256=instance.get("ChecksumSHA256"),
            ServerSideEncryption=instance.get("ServerSideEncryption"),
            VersionId=instance.get("VersionId"),
            SSECustomerAlgorithm=instance.get("SSECustomerAlgorithm"),
            SSECustomerKeyMD5=instance.get("SSECustomerKeyMD5"),
            SSEKMSKeyId=instance.get("SSEKMSKeyId"),
            SSEKMSEncryptionContext=instance.get("SSEKMSEncryptionContext"),
            BucketKeyEnabled=instance.get("BucketKeyEnabled"),
            Size=instance.get("Size"),
            RequestCharged=instance.get("RequestCharged")
            )

    def to_dict(self) -> Dict:
        return asdict(self)
