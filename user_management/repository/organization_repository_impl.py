"""This module contains the implementation of Organization repository"""
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.organization_repository import OrganizationRepository
from user_management.contract.to.user_organization_role_to import UserOrganizationRoleTO
from user_management.contract.to.user_organization_to import UserOrganizationTO
from user_management.contract.to.organization_to import OrganizationTO
from user_management.models import Organization
from user_management.models.user_organization_role import UserOrganizationRole


class OrganizationRepositoryImpl(OrganizationRepository):

    def get_user_organizations_by_filters(self, **kwargs):
        filters = {key: value for key, value in kwargs.items() if value is not None}
        organization_users = UserOrganizationRole.objects.filter(**filters)
        return UserOrganizationRoleTO.from_models(organization_users)

    def get_organization_users_by_organization_id(self, organization_id):
        organization_users = UserOrganizationRole.objects.filter(organization_id=organization_id)
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

    def invite_user_to_organization(self, data):
        UserOrganizationRole.objects.create(data)
