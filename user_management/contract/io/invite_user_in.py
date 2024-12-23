"""Request object to invite user contract"""
from rest_framework import serializers


class InviteUserIn(serializers.Serializer):
    """Invite user contract"""
    email = serializers.CharField(required=True, allow_null=False)
    id = serializers.UUIDField(required=True, allow_null=False)
    role_id = serializers.IntegerField(allow_null=True)
