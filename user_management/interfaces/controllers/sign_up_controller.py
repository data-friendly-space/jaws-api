from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up_controller(request):
    user_service = UsersServiceImpl()
    name = request.data.get('name')
    lastname = request.data.get('lastname')
    password = request.data.get('password')
    email = request.data.get('email')
    return user_service.sign_up(name, lastname, email, password)
