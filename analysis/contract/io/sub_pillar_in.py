"""This module contains the entry serializer"""
from rest_framework import serializers


class SubPillarIn(serializers.Serializer):
    """
    Serializer to transform SubPillar JSON to Dict format.
    """
    id = serializers.IntegerField(required=True)
    name = serializers.CharField()
    alias = serializers.CharField(required=False,allow_null=True)

