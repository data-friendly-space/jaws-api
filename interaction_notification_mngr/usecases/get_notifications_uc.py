"""This module contains the get notifications use case"""
from common.helpers.query_options import QueryOptions
from interaction_notification_mngr.contract.repository.notification_repository import NotificationRepository


class GetNotificationsUC:
    """Retrieves the notifications"""
    _instance = None

    def __init__(self):
        if GetNotificationsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetNotificationsUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if GetNotificationsUC._instance is None:
            GetNotificationsUC()
        return GetNotificationsUC._instance

    def exec(self, repository: NotificationRepository, query_options: QueryOptions, **kwargs):
        """Execute the use case"""
        return repository.get_all(query_options, **kwargs)
