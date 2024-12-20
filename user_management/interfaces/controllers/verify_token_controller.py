from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from common.helpers.api_responses import api_response_success
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['GET'])
@authentication_classes([])  # Disable default authentication classes
@permission_classes([])  # Disable default permissions
def verify_token_controller(request):
    """
    Endpoint to verify if the access token is valid.
    Returns a boolean indicating if the user is authenticated.
    """
    user_service = UsersServiceImpl()
    # Extract the token from the Authorization header
    auth_header = request.headers.get('Authorization', None)
    user_service.verify_token(auth_header)
    return api_response_success("Is authenticated", {'isAuthenticated': True}, status.HTTP_200_OK)
