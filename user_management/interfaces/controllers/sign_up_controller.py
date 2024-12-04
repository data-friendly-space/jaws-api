from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from common.helpers.api_responses import api_response_success
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
@authentication_classes([])  # Disable default authentication classes
@permission_classes([])  # Disable default permissions
def sign_up_controller(request):
    user_service = UsersServiceImpl()
    name = request.data.get('name')
    lastname = request.data.get('lastname')
    password = request.data.get('password')
    email = request.data.get('email')
    user_service.sign_up(name, lastname, email, password)
    return api_response_success("User successfully created", None, status.HTTP_201_CREATED)
