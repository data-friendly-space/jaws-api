"""This module contains the role serializer"""
from rest_framework import serializers


class PermissionSerializer(serializers.Serializer):
    """Serializer for the Permission model."""
    id = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()


class RoleSerializer(serializers.Serializer):
    """Serializer for the Role model."""
    id = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()
    permissions = PermissionSerializer(many=True, read_only=True)
