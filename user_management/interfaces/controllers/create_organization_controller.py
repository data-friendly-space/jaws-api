from rest_framework import status
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from user_management.contract.io.create_organization_in import CreateOrganizationIn
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


@api_view(['POST'])
def create_organization_controller(request):
    """
    return OrganizationTO.
    """
    service = OrganizationServiceImpl()
    create_organization_in = CreateOrganizationIn(data=to_snake_case_data(request.data))

    return api_response_success("Organization created successfully",
                                service.create_organization(create_organization_in),
                                status.HTTP_201_CREATED)
