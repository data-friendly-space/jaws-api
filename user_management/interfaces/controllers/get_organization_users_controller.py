from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


@api_view(['GET'])
def get_organization_users_controller(request, organization_id):
    """
    return UserOrganizationTO.
    """
    service = OrganizationServiceImpl()

    return api_response_success("Organization users retrieved successfully",
                                service.get_organization_users_by_organization_id(organization_id),
                                status.HTTP_200_OK)
