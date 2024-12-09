from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.users_service_impl import UsersServiceImpl
from user_management.service.workspace_service import WorkspaceService


@api_view(['POST'])
def create_workspace_controller(request):
    """
    return WorkspaceTO.
    """
    workspace_service = WorkspaceService()

    return api_response_success("Users retrieved successfully", workspace_service.get_workspace(query_options),
                                status.HTTP_200_OK)
