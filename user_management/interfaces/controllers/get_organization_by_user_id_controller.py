from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


@api_view(['GET'])
def get_organization_by_user_id_controller(request, user_id):
    """
    return OrganizationTO.
    """
    service = OrganizationServiceImpl()

    return api_response_success("Organizations retrieved successfully", service.get_organizations_by_user_id(user_id),
                                status.HTTP_200_OK)
