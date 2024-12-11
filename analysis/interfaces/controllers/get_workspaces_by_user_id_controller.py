"""This module contain the creation workspace controller"""
from rest_framework import status
from rest_framework.decorators import api_view


from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


@api_view(["POST"])
def create_workspace_controller(request):
    """Create a new workspace"""
    service = WorkspaceServiceImpl()

    return api_response_success("Success", service.create_workspace(create_workspace_in, request.user.id),
                                status.HTTP_201_CREATED)
