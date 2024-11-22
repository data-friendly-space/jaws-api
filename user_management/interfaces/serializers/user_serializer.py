from rest_framework import serializers

from user_management.models import User


class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField()
    position = serializers.JSONField()
    affiliation = serializers.JSONField()
    organization = serializers.JSONField()
    uiConfiguration = serializers.JSONField()
    profileImage = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'name', 'lastname', 'email', 'country',
            'profileImage', 'position', 'affiliation',
            'organization', 'uiConfiguration'
        ]
