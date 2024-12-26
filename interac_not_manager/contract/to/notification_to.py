"""This module contains the disaggregation Transfer Object"""
import datetime
from dataclasses import dataclass

from interac_not_manager.models.notification import Notification
from common.contract.to.base_to import BaseTO


@dataclass
class NotificationTO(BaseTO):
    """Notification TO"""
    id: int
    userId: str
    message: str
    createdAt: datetime
    read: bool
    type: str

    @classmethod
    def from_model(cls, instance: Notification):
        """Transforms Notification instance into a Notification TO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            userId=str(instance.user_id),
            message=instance.message,
            createdAt=instance.created_at,
            read=instance.read,
            type=instance.type
        )

    @classmethod
    def from_models(cls, notifications):
        """Create a notification TO based on a database model"""
        if notifications is None or notifications.count() <= 0:
            return None
        return [cls.from_model(notification) for notification in notifications.all()]
