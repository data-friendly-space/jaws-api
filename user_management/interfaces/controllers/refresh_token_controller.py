from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
def refresh_token_controller(request):
    """
    Handles refreshing the access token using a valid refresh token.

    Request Body:
    - refresh: The refresh token provided during authentication.

    Response:
    - 200: Returns a new access token if the refresh token is valid.
    - 401: Returns an error message if the refresh token is invalid or expired.
    """

    user_service = UsersServiceImpl()
    return api_response_success(
        "Access granted", {"jwt_access_token": user_service.refresh_token(request.data.get('refresh'))},
        status.HTTP_200_OK
    )
