
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework import status

from user_management.interfaces.controllers.helpers.api_response import api_response
from user_management.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up_controller(request):
    name = request.data.get('name')
    lastname = request.data.get('lastname')
    password = request.data.get('password')
    email = request.data.get('email')

    if not email or not password or not email:
        return api_response("All fields are mandatory", None, status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return api_response("User already exists", None, status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        lastname=lastname,
        name=name,
        email=email,
        password=make_password(password)
    )

    return api_response("User successfully created", status.HTTP_201_CREATED)
