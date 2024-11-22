from rest_framework import serializers

from user_management.models import Role


class RoleTO(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


