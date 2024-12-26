from rest_framework import status
from rest_framework.decorators import api_view

from user_management.contract.io.sign_in_in import SignInIn
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
def sign_in_controller(request):
    user_service = UsersServiceImpl()
    sign_in_in = SignInIn(data=to_snake_case_data(request.data))
    return api_response_success("User authenticated", user_service.sign_in(sign_in_in), status.HTTP_200_OK)
