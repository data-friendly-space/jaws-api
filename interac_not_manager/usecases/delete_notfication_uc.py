"""This module contains the get notifications use case"""
from common.helpers.query_options import QueryOptions
from interac_not_manager.contract.repository.notification_repository import NotificationRepository


class DeleteNotificationUC:
    """Retrieves the notifications"""
    _instance = None

    def __init__(self):
        if DeleteNotificationUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DeleteNotificationUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if DeleteNotificationUC._instance is None:
            DeleteNotificationUC()
        return DeleteNotificationUC._instance

    def exec(self, repository: NotificationRepository, notification_id: int):
        """Execute the use case"""
        return repository.delete_by_id(notification_id)
