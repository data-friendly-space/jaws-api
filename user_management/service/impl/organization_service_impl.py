"""This module contains the organization service implementation"""

from common.exceptions.exceptions import BadRequestException
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_organization_in import CreateOrganizationIn
from user_management.contract.io.invite_user_organization_in import InviteUserOrganizationIn
from user_management.repository.organization_repository_impl import OrganizationRepositoryImpl
from user_management.service.organization_service import OrganizationService
from user_management.usecases.create_organization_uc import CreateOrganizationUC
from user_management.usecases.get_organization_users_by_organization_id_uc import GetOrganizationUsersByOrganizationIdUC
from user_management.usecases.get_user_organizations_by_filters_uc import GetUserOrganizationsByFiltersUC
from user_management.usecases.invite_user_to_workspace_uc import InviteUserToWorkspaceUC


class OrganizationServiceImpl(OrganizationService):
    """Organization service implementation"""

    def __init__(self):
        self.get_all_organizations_uc = GetAllUC.get_instance()
        self.create_organization_uc = CreateOrganizationUC.get_instance()
        self.get_user_organizations_by_filter_uc = GetUserOrganizationsByFiltersUC.get_instance()
        self.get_organizations_users_by_organization_id = GetOrganizationUsersByOrganizationIdUC.get_instance()
        self.invite_user_to_organization_uc = InviteUserToWorkspaceUC.get_instance()
        self.organization_repository = self.organization_repository

    def get_organizations(self):
        """Retrieves the organizations"""
        organizations = self.get_all_organizations_uc.exec(self.organization_repository)
        return [organization.to_dict() for organization in organizations]

    def create_organization(self, create_organization_in: CreateOrganizationIn):
        """Create a new organization"""
        if not create_organization_in.is_valid():
            raise BadRequestException("Organization request is not valid: ", create_organization_in.errors)
        data = create_organization_in.validated_data

        return self.create_organization_uc.exec(self.organization_repository, data).to_dict()

    def get_organizations_by_user_id(self, user_id: str):
        """Returns a list of organizations with user role based on user id """
        organizations = self.get_user_organizations_by_filter_uc.exec(self.organization_repository, user_id=user_id)
        return [organization.to_dict() for organization in organizations]

    def get_organization_users_by_organization_id(self, organization_id: str):
        """Returns a list of organizations based on organization id """
        organizations = self.get_organizations_users_by_organization_id.exec(self.organization_repository,
                                                                             organization_id=organization_id)
        return [organization.to_dict() for organization in organizations]

    def invite_user_to_organization(self, invite_user_in: InviteUserOrganizationIn):
        if not invite_user_in.is_valid():
            raise BadRequestException("Invite user request is not valid: ", invite_user_in.errors)
        data = invite_user_in.validated_data
        self.invite_user_to_organization_uc.exec(self.organization_repository, data)
