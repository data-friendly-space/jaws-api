from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


@api_view(['GET'])
def get_users_from_organization_by_role_controller(request, organization_id, role):
    """
    return UserOrganizationTO.
    """
    service = OrganizationServiceImpl()

    return api_response_success("Users from org retrieved successfully",
                                service.get_organization_users_by_role(organization_id, role),
                                status.HTTP_200_OK)
