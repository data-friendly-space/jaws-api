"""This module contains the user serializer"""
from rest_framework import serializers

from user_management.interfaces.serializers.affiliation_serializer import AffiliationSerializer
from user_management.interfaces.serializers.organization_serializer import OrganizationSerializer
from user_management.interfaces.serializers.position_serializer import PositionSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField
    name = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField(allow_null=True, allow_blank=True)
    position = PositionSerializer(allow_null=True)
    affiliation = AffiliationSerializer(allow_null=True)
    organization = OrganizationSerializer(allow_null=True)
    uiConfiguration = serializers.JSONField(required=False, allow_null=True)
    profileImage = serializers.CharField(required=False, allow_null=True)
