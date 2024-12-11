"""This module contains the organization service implementation"""

from common.exceptions.exceptions import BadRequestException
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_organization_in import CreateOrganizationIn
from user_management.interfaces.serializers.organization_serializer import OrganizationSerializer
from user_management.repository.organization_repository_impl import OrganizationRepositoryImpl
from user_management.service.organization_service import OrganizationService
from user_management.usecases.create_organization_uc import CreateOrganizationUC


class OrganizationServiceImpl(OrganizationService):
    """Organization service implementation"""

    def __init__(self):
        self.get_all_organizations_uc = GetAllUC.get_instance()
        self.create_organization_uc = CreateOrganizationUC.get_instance()

    def get_organizations(self):
        """Retrieves the organizations"""
        return OrganizationSerializer(self.get_all_organizations_uc.exec(OrganizationRepositoryImpl()), many=True).data

    def create_organization(self, create_organization_in: CreateOrganizationIn):
        """Create a new organization"""
        if not create_organization_in.is_valid():
            raise BadRequestException("Organization request is not valid: ", create_organization_in.errors)
        data = create_organization_in.validated_data

        return OrganizationSerializer(self.create_organization_uc.exec(OrganizationRepositoryImpl(), data)).data

    def get_organization_users(self, organization_id):
        pass
