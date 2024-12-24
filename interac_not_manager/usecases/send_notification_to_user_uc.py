"""This module contains the get users use case"""
from interac_not_manager.contract.repository.notification_repository import NotificationRepository


class SendNotificationToUserUC:
    """Retrieves the users"""
    _instance = None

    def __init__(self):
        if SendNotificationToUserUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SendNotificationToUserUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if SendNotificationToUserUC._instance is None:
            SendNotificationToUserUC()
        return SendNotificationToUserUC._instance

    def exec(self, repository: NotificationRepository, data):
        """Execute the use case"""
        return repository.create(data)
