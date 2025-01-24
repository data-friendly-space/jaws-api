"""This module contains the sector serializer"""
from rest_framework import serializers


class IssueIn(serializers.Serializer):
    """
    Serializer to transform Issue JSON to Dict format.
    """
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=600)
    description = serializers.CharField(max_length=600)
    informationGaps = serializers.CharField(max_length=600)
    assumptions = serializers.CharField(max_length=600)
    disaggregation = serializers.IntegerField(required=False)
    entries = serializers.ListField(child=serializers.IntegerField())
    charts = serializers.ListField(child=serializers.IntegerField())
    analysisId = serializers.IntegerField(required=True)
