from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status

from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['GET'])
def verify_token_view(request):
    """
    Endpoint to verify if the access token is valid.
    Returns a boolean indicating if the user is authenticated.
    """
    user_service = UsersServiceImpl()
    # Extract the token from the Authorization header
    auth_header = request.headers.get('Authorization', None)

    return user_service.verify_token(auth_header)
