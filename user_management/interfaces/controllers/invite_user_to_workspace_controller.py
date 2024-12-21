from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.contract.io.invite_user_workspace_in import InviteUserWorkspaceIn
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


@api_view(['POST'])
def invite_user_to_workspace_controller(request):
    """
    Link a user with role to a workspace
    """
    service = WorkspaceServiceImpl()
    invite_user_workspace_in = InviteUserWorkspaceIn(data=to_snake_case_data(request.data))

    return api_response_success("User invited successfully",
                                service.invite_user_to_workspace(invite_user_workspace_in),
                                status.HTTP_200_OK)
