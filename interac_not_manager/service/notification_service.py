"""This module contains the notification service"""
from abc import ABC, abstractmethod

from common.helpers.query_options import QueryOptions
from user_management.models import User


class NotificationService(ABC):
    """Notification service"""
    @abstractmethod
    def get_user_notifications(self, query_options: QueryOptions, user_id: str):
        """Retrieves the notifications"""
        pass

