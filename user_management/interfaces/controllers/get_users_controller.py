"""Contains the controller for getting all the users"""
from rest_framework import status
from rest_framework.decorators import api_view


from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(["GET"])
def get_users_controller(request):
    """
    List all users and return them in UserTO format.
    """
    users_service = UsersServiceImpl()
    query_options = QueryOptions.from_request(request)

    return api_response_success(
        "Users retrieved successfully",
        users_service.get_users(query_options),
        status.HTTP_200_OK,
    )
