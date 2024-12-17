from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


@api_view(['GET'])
def get_organizations_users_by_user_id_controller(request):
    """
    return UserOrganizationTO.
    """
    service = OrganizationServiceImpl()
    query_options = QueryOptions.from_request(request)
    return api_response_success("Organization users retrieved successfully",
                                service.get_organizations_users_by_user_id(request.user.id, query_options),
                                status.HTTP_200_OK)
