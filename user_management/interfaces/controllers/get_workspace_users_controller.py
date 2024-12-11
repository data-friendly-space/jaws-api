from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


@api_view(['GET'])
def get_workspace_users_controller(request, workspace_id):
    """
    return UserWorkspaceTO.
    """
    service = WorkspaceServiceImpl()

    return api_response_success("Workspace users retrieved successfully",
                                service.get_workspace_users_by_workspace_id(workspace_id),
                                status.HTTP_200_OK)