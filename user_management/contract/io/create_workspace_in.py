"""Request object to create an Workspace contract"""
from rest_framework import serializers

from common.test_utils import User


class CreateWorkspaceIn(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    facilitator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    country = serializers.CharField(max_length=100)
