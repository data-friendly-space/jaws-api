"""Request object to create an Workspace contract"""
from rest_framework import serializers


class InviteUserWorkspaceIn(serializers.Serializer):
    user_id: serializers.UUIDField(allow_null=False)
    workspace_id: serializers.UUIDField(allow_null=False)
    role_id: serializers.UUIDField(allow_null=False)
