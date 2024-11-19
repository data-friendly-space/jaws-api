from rest_framework import status
from rest_framework.decorators import api_view

from user_management.interfaces.controllers.helpers.api_response import api_response
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['GET'])
def get_users_controller(request):
    """
    List all users and return them in UserTO format.
    """
    try:
        users_service = UsersServiceImpl()
        serialized_users = UserSerializer(users_service.get_users(), many=True).data
        return api_response("Users retrieved successfully", serialized_users, status.HTTP_200_OK)
    except Exception as e:
        return api_response(str(e), [], status.HTTP_500_INTERNAL_SERVER_ERROR)
