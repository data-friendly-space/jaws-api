"""This module contains the user serializer"""
from rest_framework import serializers

from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.models import Workspace


class WorkspaceSerializer(serializers.Serializer):
    """Serialize the user model into a TO"""
    id = serializers.CharField(max_length=36)
    title = serializers.CharField(max_length=200)
    creation_date = serializers.DateTimeField()
    last_access_date = serializers.DateTimeField()
    facilitator = UserSerializer()
    country = serializers.CharField(max_length=100)
    analysis = None

    class Meta:
        """Base class"""
        model = Workspace
        fields = [
            'id', 'name', 'lastname', 'email', 'country',
            'profileImage', 'position', 'affiliation',
            'organization', 'uiConfiguration'
        ]
