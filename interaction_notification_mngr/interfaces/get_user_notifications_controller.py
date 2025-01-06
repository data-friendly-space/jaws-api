from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from interaction_notification_mngr.service.impl.notification_service_impl import NotificationServiceImpl


@api_view(['GET'])
def get_user_notifications_controller(request):
    """controller to retrieve all user notifications"""
    service = NotificationServiceImpl()
    query_options = QueryOptions.from_request(request)
    return api_response_success("User notifications retrieve successfully",
                                service.get_user_notifications(query_options, request.user.id),
                                status.HTTP_200_OK)
