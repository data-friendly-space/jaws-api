from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.role_service_impl import RoleServiceImpl


@api_view(['GET'])
def get_roles_and_permissions_controller(request):
    """
    List all roles and permissions then return them in RoleTO format.
    """
    roles_service = RoleServiceImpl()
    return api_response_success("Roles retrieved successfully", roles_service.get_roles_and_permissions(),
                                status.HTTP_200_OK)
