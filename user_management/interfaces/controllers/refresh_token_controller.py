from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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
    return user_service.refresh_token(request.data.get('refresh'))
