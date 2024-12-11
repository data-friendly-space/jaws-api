from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


@api_view(['GET'])
def get_workspace_by_user_id_controller(request, user_id):
    """
    return WorkspaceTO.
    """
    service = WorkspaceServiceImpl()

    return api_response_success("Workspaces retrieved successfully", service.get_workspaces_by_user_id(user_id),
                                status.HTTP_200_OK)
