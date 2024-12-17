from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.contract.io.sign_up_in import SignUpIn
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
def sign_up_controller(request):
    user_service = UsersServiceImpl()

    sign_up_in = SignUpIn(data=to_snake_case_data(request.data))
    user_service.sign_up(sign_up_in)
    return api_response_success("User successfully created", None, status.HTTP_201_CREATED)
