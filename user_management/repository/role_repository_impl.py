"""This module contains the implementation of Role repository"""
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.role_repository import RoleRepository
from user_management.contract.to.permission_to import PermissionTO
from user_management.contract.to.role_to import RoleTO
from user_management.models import Role


class RoleRepositoryImpl(RoleRepository):
    """Repository implementation for Role repository"""

    def get_role_by_role(self, role) -> RoleTO:
        """Retrieve role by role"""
        return RoleTO.from_model(Role.objects.filter(role=role).first())

    def delete_by_id(self, obj_id):
        """Delete role by id"""
        role = Role.objects.get(id=obj_id)
        return role.delete()

    def update(self, obj_id, data):
        """Update role by ID"""
        role = Role.objects.get(id=obj_id)
        for field, value in data.items():
            setattr(role, field, value)
        role.save()
        return role

    def get_by_id(self, obj_id) -> RoleTO:
        """Retrieve role by ID"""
        return RoleTO.from_model(Role.objects.filter(id=obj_id).first())

    def create(self, data):
        """Creates and retrieve new role"""
        return RoleTO.from_model(Role.objects.create(data))

    def get_all(self, query_options: QueryOptions) -> list[RoleTO]:
        """Retrieves all roles"""
        roles = Role.objects.exclude()
        return RoleTO.from_models(roles)

    def get_roles(self, exclusions) -> list[RoleTO]:
        """Retrieves all roles"""
        roles = Role.objects.exclude(role__in=exclusions)
        return RoleTO.from_models(roles)


