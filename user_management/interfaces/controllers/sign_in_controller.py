from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from common.helpers.api_responses import api_response_success
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
@authentication_classes([])  # Disable default authentication classes
@permission_classes([])  # Disable default permissions
def sign_in_controller(request):
    user_service = UsersServiceImpl()
    email = request.data.get('email')
    password = request.data.get('password')
    return api_response_success("User authenticated", user_service.sign_in(email, password), status.HTTP_200_OK)
