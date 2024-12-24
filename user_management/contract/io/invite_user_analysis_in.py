"""Request object to invite user contract"""
from rest_framework import serializers


class InviteUserAnalysisIn(serializers.Serializer):
    """Invite user contract"""
    email = serializers.CharField(required=True, allow_null=False)
    id = serializers.IntegerField(required=True, allow_null=False)
    role_id = serializers.IntegerField(allow_null=True)
