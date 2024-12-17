"""This module contains the implementation of Organization repository"""
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.organization_repository import OrganizationRepository
from user_management.contract.to.organization_to import OrganizationTO
from user_management.contract.to.user_organization_role_to import UserOrganizationRoleTO
from user_management.contract.to.user_organization_to import UserOrganizationTO
from user_management.contract.to.user_to import UserTO
from user_management.models import Organization
from user_management.models.user_organization_role import UserOrganizationRole


class OrganizationRepositoryImpl(OrganizationRepository):

    def get_user_organizations_by_filters(self, query_options: QueryOptions, **kwargs):
        filters = {key: value for key, value in kwargs.items() if value is not None}
        organization_users = UserOrganizationRole.objects.filter(**filters)
        if query_options:
            organization_users = query_options.filter_and_exec_queryset(organization_users, model=UserOrganizationRole)
        if not organization_users or len(organization_users) == 0:
            return []
        return UserOrganizationRoleTO.from_models(organization_users)

    def get_organizations_users_by_user_id(self, query_options: QueryOptions, **kwargs):
        filters = {key: value for key, value in kwargs.items() if value is not None}
        user_organizations = UserOrganizationRole.objects.filter(**filters)
        organization_users = UserOrganizationRole.objects.filter(
            organization__id__in=user_organizations.values_list('organization', flat=True)).select_related('user',
                                                                                                           'role',
                                                                                                           'organization')
        if query_options:
            organization_users = query_options.filter_and_exec_queryset(organization_users, model=UserOrganizationRole)
        if not organization_users or len(organization_users) == 0:
            return []
        return UserOrganizationTO.from_models(organization_users)

    def delete_by_id(self, obj_id):
        """Delete organization by id"""
        organization = Organization.objects.get(id=obj_id)
        return organization.delete()

    def update(self, obj_id, data):
        """Update organization by ID"""
        organization = Organization.objects.get(id=obj_id)
        for field, value in data.items():
            setattr(organization, field, value)
        organization.save()
        return organization

    def get_by_id(self, obj_id):
        """Retrieve organization by ID"""
        return Organization.objects.filter(id=obj_id).first()

    def create(self, data):
        """Creates and retrieve new organization"""
        organization = Organization.objects.create(**data)
        return OrganizationTO.from_model(organization)

    def get_all(self, query_options: QueryOptions):
        """Retrieves all organizations"""
        return OrganizationTO.from_models(Organization.objects.all())


    def get_available_organizations_by_user_id(self, user_id: str):
        organization_users = UserOrganizationRole.objects.filter(user_id=user_id)
        return [OrganizationTO.from_model(organization_user.organization) for organization_user in organization_users]

    def get_users_from_organization_by_role(self, organization_id: str, role_id: str):
        organization_users = UserOrganizationRole.objects.filter(organization_id=organization_id, role_id=role_id)
        return [UserTO.from_model(organization_user.user) for organization_user in organization_users]
