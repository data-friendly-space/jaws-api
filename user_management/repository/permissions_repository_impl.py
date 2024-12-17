"""This module contains the implementation of Permission repository"""
from user_management.contract.repository.permission_repository import PermissionRepository

from common.helpers.query_options import QueryOptions
from user_management.contract.to.permission_to import PermissionTO
from user_management.models import Permission


class PermissionRepositoryImpl(PermissionRepository):
    """Repository implementation for Permission repository"""

    def delete_by_id(self, obj_id):
        """Delete permission by id"""
        permission = Permission.objects.get(id=obj_id)
        return permission.delete()

    def update(self, obj_id, data):
        """Update permission by ID"""
        permission = Permission.objects.get(id=obj_id)
        for field, value in data.items():
            setattr(permission, field, value)
        permission.save()
        return permission

    def get_by_id(self, obj_id) -> PermissionTO:
        """Retrieve permission by ID"""
        return PermissionTO.from_model(Permission.objects.filter(id=obj_id).first())

    def create(self, data):
        """Creates and retrieve new permission"""
        return PermissionTO.from_model(Permission.objects.create(data))

    def get_all(self, query_options: QueryOptions) -> list[PermissionTO]:
        """Retrieves all permissions"""
        permissions = Permission.objects.exclude()
        return PermissionTO.from_models(permissions)
