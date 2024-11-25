from rest_framework import serializers

from user_management.models import Organization


class OrganizationTO(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

