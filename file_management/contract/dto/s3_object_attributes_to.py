"""Contains the DTO for S3 Object attributes"""
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional, Dict

from common.contract.to.base_to import BaseTO

@dataclass
class S3ObjectAttributesTO(BaseTO):
    """DTO for S3 object attributes"""
    Body: Optional[object] = None
    DeleteMarker: Optional[bool] = None
    AcceptRanges: Optional[str] = None
    Expiration: Optional[str] = None
    Restore: Optional[str] = None
    LastModified: Optional[datetime] = None
    ContentLength: Optional[int] = None
    ETag: Optional[str] = None
    ChecksumCRC32: Optional[str] = None
    ChecksumCRC32C: Optional[str] = None
    ChecksumSHA1: Optional[str] = None
    ChecksumSHA256: Optional[str] = None
    MissingMeta: Optional[int] = None
    VersionId: Optional[str] = None
    CacheControl: Optional[str] = None
    ContentDisposition: Optional[str] = None
    ContentEncoding: Optional[str] = None
    ContentLanguage: Optional[str] = None
    ContentRange: Optional[str] = None
    ContentType: Optional[str] = None
    Expires: Optional[datetime] = None
    ExpiresString: Optional[str] = None
    WebsiteRedirectLocation: Optional[str] = None
    ServerSideEncryption: Optional[str] = None
    Metadata: Dict[str, str] = field(default_factory=dict)
    SSECustomerAlgorithm: Optional[str] = None
    SSECustomerKeyMD5: Optional[str] = None
    SSEKMSKeyId: Optional[str] = None
    BucketKeyEnabled: Optional[bool] = None
    StorageClass: Optional[str] = None
    RequestCharged: Optional[str] = None
    ReplicationStatus: Optional[str] = None
    PartsCount: Optional[int] = None
    TagCount: Optional[int] = None
    ObjectLockMode: Optional[str] = None
    ObjectLockRetainUntilDate: Optional[datetime] = None
    ObjectLockLegalHoldStatus: Optional[str] = None

    @classmethod
    def from_model(cls, instance: dict) -> 'S3ObjectAttributesTO':
        return cls(
            Body=instance.get('Body'),
            DeleteMarker=instance.get('DeleteMarker'),
            AcceptRanges=instance.get('AcceptRanges'),
            Expiration=instance.get('Expiration'),
            Restore=instance.get('Restore'),
            LastModified=instance.get('LastModified'),
            ContentLength=instance.get('ContentLength'),
            ETag=instance.get('ETag'),
            ChecksumCRC32=instance.get('ChecksumCRC32'),
            ChecksumCRC32C=instance.get('ChecksumCRC32C'),
            ChecksumSHA1=instance.get('ChecksumSHA1'),
            ChecksumSHA256=instance.get('ChecksumSHA256'),
            MissingMeta=instance.get('MissingMeta'),
            VersionId=instance.get('VersionId'),
            CacheControl=instance.get('CacheControl'),
            ContentDisposition=instance.get('ContentDisposition'),
            ContentEncoding=instance.get('ContentEncoding'),
            ContentLanguage=instance.get('ContentLanguage'),
            ContentRange=instance.get('ContentRange'),
            ContentType=instance.get('ContentType'),
            Expires=instance.get('Expires'),
            ExpiresString=instance.get('ExpiresString'),
            WebsiteRedirectLocation=instance.get('WebsiteRedirectLocation'),
            ServerSideEncryption=instance.get('ServerSideEncryption'),
            Metadata=instance.get('Metadata', {}),
            SSECustomerAlgorithm=instance.get('SSECustomerAlgorithm'),
            SSECustomerKeyMD5=instance.get('SSECustomerKeyMD5'),
            SSEKMSKeyId=instance.get('SSEKMSKeyId'),
            BucketKeyEnabled=instance.get('BucketKeyEnabled'),
            StorageClass=instance.get('StorageClass'),
            RequestCharged=instance.get('RequestCharged'),
            ReplicationStatus=instance.get('ReplicationStatus'),
            PartsCount=instance.get('PartsCount'),
            TagCount=instance.get('TagCount'),
            ObjectLockMode=instance.get('ObjectLockMode'),
            ObjectLockRetainUntilDate=instance.get('ObjectLockRetainUntilDate'),
            ObjectLockLegalHoldStatus=instance.get('ObjectLockLegalHoldStatus')
        )

    def to_dict(self):
        return asdict(self)
