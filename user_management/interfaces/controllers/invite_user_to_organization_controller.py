from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.contract.io.invite_user_in import InviteUserIn
from user_management.service.impl.users_service_impl import UsersServiceImpl


@api_view(['POST'])
def invite_user_to_organization_controller(request):
    """
    Link a user with role to a organization
    """
    service = UsersServiceImpl()
    invite_user_organization_in = InviteUserIn(data=to_snake_case_data(request.data))
    return api_response_success("Invite user to organization successfully",
                                service.invite_user_to_org(invite_user_organization_in),
                                status.HTTP_200_OK)
