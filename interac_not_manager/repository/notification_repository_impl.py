"""This module contains the implementation of Notification repository"""
from common.helpers.query_options import QueryOptions
from interac_not_manager.contract.repository.notification_repository import NotificationRepository
from interac_not_manager.contract.to.notification_to import NotificationTO
from interac_not_manager.models.notification import Notification


class NotificationRepositoryImpl(NotificationRepository):
    """Repository implementation for Notification repository"""

    def delete_by_id(self, obj_id):
        """Delete notification by id"""
        notification = Notification.objects.get(id=obj_id)
        return notification.delete()

    def update(self, obj_id, data):
        """Update notification by ID"""
        notification = Notification.objects.get(id=obj_id)
        for field, value in data.items():
            setattr(notification, field, value)
        notification.save()
        return notification

    def get_by_id(self, obj_id) -> NotificationTO:
        """Retrieve notification by ID"""
        return NotificationTO.from_model(Notification.objects.filter(id=obj_id).first())

    def create(self, data):
        """Creates and retrieve new notification"""
        data['type'] = "info"
        return NotificationTO.from_model(Notification.objects.create(**data))

    def get_all(self, query_options: QueryOptions, **kwargs) -> list[NotificationTO]:
        """Retrieves all notifications"""
        filters = {key: value for key, value in kwargs.items() if value is not None}
        notifications = Notification.objects.filter(**filters)
        if query_options:
            notifications = query_options.filter_and_exec_queryset(notifications, model=Notification)
        return [] if not notifications or len(notifications) == 0 else NotificationTO.from_models(notifications)
