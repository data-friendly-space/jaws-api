from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


@api_view(['POST'])
def create_workspace_controller(request):
    """
    return WorkspaceTO.
    """
    service = WorkspaceServiceImpl()
    create_workspace_in = CreateWorkspaceIn(data=to_snake_case_data(request.data))

    return api_response_success("Organization retrieved successfully", service.create_workspace(create_workspace_in),
                                status.HTTP_200_OK)
