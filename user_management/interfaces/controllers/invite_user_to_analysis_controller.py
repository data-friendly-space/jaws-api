from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.contract.io.invite_user_in import InviteUserIn
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
def invite_user_to_analysis_controller(request):
    """
    Link a user with role to a workspace
    """
    service = UsersServiceImpl()
    invite_user_analysis_in = InviteUserIn(data=to_snake_case_data(request.data))

    return api_response_success("User invited successfully",
                                service.invite_user_to_analysis(invite_user_analysis_in),
                                status.HTTP_200_OK)
