"""This module contains the entry serializer"""
from rest_framework import serializers

from analysis.contract.io.sub_pillar_in import SubPillarIn


class CreateEntryIn(serializers.Serializer):
    """
    Serializer to transform Entry JSON to Dict format.
    """
    fragment = serializers.CharField()
    source = serializers.CharField()
    createdAt = serializers.DateTimeField()
    createdBy = serializers.CharField()
    tag = SubPillarIn()
