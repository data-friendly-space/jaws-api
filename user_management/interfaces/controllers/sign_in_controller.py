from rest_framework.decorators import api_view, permission_classes, authentication_classes

from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
@authentication_classes([])  # Disable default authentication classes
@permission_classes([])  # Disable default permissions
def sign_in_controller(request):
    user_service = UsersServiceImpl()
    email = request.data.get('email')
    password = request.data.get('password')
    return user_service.sign_in(email, password)
