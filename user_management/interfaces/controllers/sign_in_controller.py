from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user_management.interfaces.controllers.helpers.api_response import api_response
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in_controller(request):
    user_service = UsersServiceImpl()
    email = request.data.get('email')
    password = request.data.get('password')
    return user_service.sign_in(email, password)
