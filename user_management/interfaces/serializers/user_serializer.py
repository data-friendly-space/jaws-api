"""This module contains the user serializer"""
from rest_framework import serializers

from user_management.models import User


class UserSerializer(serializers.Serializer):
    """Serialize the user model into a DTO"""
    id = serializers.CharField(max_length=36)
    name = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField()
    uiConfiguration = serializers.JSONField()
    profileImage = serializers.CharField(required=False, allow_null=True)

    class Meta:
        """Base class"""
        model = User
        fields = [
            'id', 'name', 'lastname', 'email', 'country',
            'profileImage', 'position', 'affiliation',
            'organization', 'uiConfiguration'
        ]
