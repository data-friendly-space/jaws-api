from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from interaction_notification_mngr.service.impl.notification_service_impl import NotificationServiceImpl


@api_view(['DELETE'])
def delete_notification_by_id_controller(request, notification_id):
    """controller to retrieve all user notifications"""
    service = NotificationServiceImpl()
    return api_response_success("Notification deleted successfully",
                                service.delete_notification(notification_id),
                                status.HTTP_200_OK)
