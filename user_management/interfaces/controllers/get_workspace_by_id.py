"""Contains the controller for getting a workspace by id"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl

@api_view(["GET"])
def get_workspaces_by_id_controller(request, workspace_id):
    """Retrieve the workspace of the given id"""
    if not workspace_id:
        raise BadRequestException("The id is required.")
    service = WorkspaceServiceImpl()
    workspace_to = service.get_workspace_by_id(request.user, workspace_id)
    return api_response_success(data = workspace_to)
