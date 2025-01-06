"""This module contains the notification service"""

from common.helpers.query_options import QueryOptions
from interaction_notification_mngr.repository.notification_repository_impl import NotificationRepositoryImpl
from interaction_notification_mngr.service.notification_service import NotificationService
from interaction_notification_mngr.usecases.delete_notfication_uc import DeleteNotificationUC
from interaction_notification_mngr.usecases.get_notifications_uc import GetNotificationsUC


class NotificationServiceImpl(NotificationService):
    """Notification service"""

    def __init__(self):
        self.get_notifications_uc = GetNotificationsUC.get_instance()
        self.delete_notification_uc = DeleteNotificationUC.get_instance()
        self.repository = NotificationRepositoryImpl()

    def get_user_notifications(self, query_options: QueryOptions, user_id: str):
        """Get user notifications"""
        notifications = self.get_notifications_uc.exec(self.repository, query_options, user_id=user_id)
        return [notification.to_dict() for notification in notifications]

    def delete_notification(self, notification_id: int):
        """Delete notification by ID"""
        self.delete_notification_uc.exec(self.repository, notification_id)
