"""This module contains the role serializer"""
from rest_framework import serializers

from user_management.models import Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for the Permission model."""

    class Meta:
        """Meta class. """
        model = Permission
        fields = ['id', 'name', 'type']


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Role model."""
    id = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        """Meta class. """
        model = Role
        fields = ['id', 'role', 'permissions']
