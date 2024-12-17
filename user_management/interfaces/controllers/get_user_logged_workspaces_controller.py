from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


@api_view(['GET'])
def get_user_logged_workspaces_controller(request):
    """
    return WorkspaceTO.
    """
    service = WorkspaceServiceImpl()
    query_options = QueryOptions.from_request(request)
    return api_response_success("Workspaces retrieved successfully", service.get_workspaces_by_user_id(request.user.id,query_options),
                                status.HTTP_200_OK)
