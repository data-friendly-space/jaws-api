"""This module contains the entry serializer"""
from rest_framework import serializers


class SubPillarIn(serializers.Serializer):
    """
    Serializer to transform SubPillar JSON to Dict format.
    """
    id = serializers.IntegerField(required=True)
    name = serializers.CharField()
    alias = serializers.CharField(required=False,allow_null=True)


class CreateEntryIn(serializers.Serializer):
    """
    Serializer to transform Entry JSON to Dict format.
    """
    fragment = serializers.CharField()
    source = serializers.CharField()
    createdAt = serializers.DateTimeField()
    createdBy = serializers.CharField()
    tag = SubPillarIn()
