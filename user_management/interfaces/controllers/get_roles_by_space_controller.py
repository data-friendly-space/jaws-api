from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.role_service_impl import RoleServiceImpl


@api_view(['GET'])
def get_roles_by_space_controller(request, space=None):
    """
    List all roles and return them in RoleTO format.
    """
    roles_service = RoleServiceImpl()
    roles = {
        "workspace": roles_service.get_workspace_roles,
        "analysis": roles_service.get_analysis_roles
    }.get(space, roles_service.get_roles)()

    return api_response_success("Roles retrieved successfully", roles,
                                status.HTTP_200_OK)
