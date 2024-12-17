from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


@api_view(['GET'])
def get_available_user_organizations(request):
    """
    return OrganizationTO filtering by user_id.
    """
    service = OrganizationServiceImpl()

    return api_response_success("Organizations retrieved successfully",
                                service.get_available_organizations_by_user_id(request.user.id),
                                status.HTTP_200_OK)
