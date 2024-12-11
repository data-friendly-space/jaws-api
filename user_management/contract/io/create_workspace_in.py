"""Request object to create an Workspace contract"""
from rest_framework import serializers


class CreateWorkspaceIn(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    facilitator_id = serializers.UUIDField(allow_null=False)
    organization_id = serializers.UUIDField(allow_null=False)
    country = serializers.CharField(max_length=100)