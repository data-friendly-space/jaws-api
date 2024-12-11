"""Request object to create an Workspace contract"""
from rest_framework import serializers


class CreateOrganizationIn(serializers.Serializer):
    name = serializers.CharField(max_length=200)
