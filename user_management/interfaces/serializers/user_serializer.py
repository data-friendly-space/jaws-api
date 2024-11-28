from rest_framework import serializers

from user_management.interfaces.serializers.affiliation_serializer import AffiliationTO
from user_management.interfaces.serializers.organization_serializer import OrganizationTO
from user_management.interfaces.serializers.position_serializer import PositionTO
from user_management.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    name = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField()
    position = PositionTO()
    affiliation = AffiliationTO()
    organization = OrganizationTO()
    uiConfiguration = serializers.JSONField()
    profileImage = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'lastname', 'email', 'country',
            'profileImage', 'position', 'affiliation',
            'organization', 'uiConfiguration'
        ]
