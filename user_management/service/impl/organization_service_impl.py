"""This module contains the organization service implementation"""

from common.exceptions.exceptions import BadRequestException
from common.helpers.query_options import QueryOptions
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_organization_in import CreateOrganizationIn
from user_management.repository.organization_repository_impl import OrganizationRepositoryImpl
from user_management.repository.role_repository_impl import RoleRepositoryImpl
from user_management.service.organization_service import OrganizationService
from user_management.usecases.create_organization_uc import CreateOrganizationUC
from user_management.usecases.get_available_organizations_by_user_id_uc import GetAvailableOrganizationsByUserIdUC
from user_management.usecases.get_organization_users_by_organization_id_uc import GetOrganizationUsersByOrganizationIdUC
from user_management.usecases.get_role_by_role_uc import GetRoleByRoleUC
from user_management.usecases.get_user_organizations_by_filters_uc import GetUserOrganizationsByFiltersUC
from user_management.usecases.get_users_from_organization_by_role import GetUserFromOrgByRoleUC


class OrganizationServiceImpl(OrganizationService):
    """Organization service implementation"""

    def __init__(self):
        self.get_all_organizations_uc = GetAllUC.get_instance()
        self.create_organization_uc = CreateOrganizationUC.get_instance()
        self.get_users_organizations_by_filter_uc = GetUserOrganizationsByFiltersUC.get_instance()
        self.get_organizations_users_by_user_id_uc = GetOrganizationUsersByOrganizationIdUC.get_instance()
        self.get_available_organizations_by_user_id_uc = GetAvailableOrganizationsByUserIdUC.get_instance()
        self.organization_repository = OrganizationRepositoryImpl()
        self.get_role_by_filters = GetRoleByRoleUC.get_instance()
        self.get_users_from_org_by_role_uc = GetUserFromOrgByRoleUC.get_instance()

    def get_organizations(self):
        """Retrieves the organizations"""
        organizations = self.get_all_organizations_uc.exec(self.organization_repository, None)
        return [organization.to_dict() for organization in organizations]

    def create_organization(self, create_organization_in: CreateOrganizationIn):
        """Create a new organization"""
        if not create_organization_in.is_valid():
            raise BadRequestException("Organization request is not valid: ", create_organization_in.errors)
        data = create_organization_in.validated_data

        return self.create_organization_uc.exec(self.organization_repository, data).to_dict()

    def get_organizations_by_user_id(self, query_options: QueryOptions, user_id: str):
        """Returns a list of organizations with user role based on user id """
        organizations = self.get_users_organizations_by_filter_uc.exec(self.organization_repository, query_options,
                                                                       user_id=user_id)
        return [organization.to_dict() for organization in organizations]

    def get_organizations_users_by_user_id(self, user_id: str, query_options: QueryOptions):
        """Returns a list of organizations based on organization id """
        organization_users = self.get_organizations_users_by_user_id_uc.exec(self.organization_repository,
                                                                             query_options,
                                                                             user_id=user_id)
        return [organization_user.to_dict() for organization_user in organization_users]


    def get_available_organizations_by_user_id(self, user_id: str):
        """Get available organizations by user_id"""
        user_organizations = self.get_available_organizations_by_user_id_uc.exec(self.organization_repository,
                                                                                 user_id=user_id)
        return [user_org.to_dict() for user_org in user_organizations]

    def get_organization_users_by_role(self, organization_id: str, role: str):
        """Returns a list of organizations with user role based on user id """
        if not role:
            raise BadRequestException("Role type must be sent")
        role_found = self.get_role_by_filters.exec(RoleRepositoryImpl(), role.upper())
        users = self.get_users_from_org_by_role_uc.exec(self.organization_repository,
                                                        organization_id,
                                                        role_found.id)
        return [user.to_dict() for user in users]
