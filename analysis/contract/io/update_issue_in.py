"""This module contains the entry serializer"""
from rest_framework import serializers


class UpdateIssueIn(serializers.Serializer):
    """
    Serializer to transform Issue JSON to Dict format.
    """
    name = serializers.CharField(max_length=600)
    description = serializers.CharField(max_length=600)
    informationGaps = serializers.CharField(max_length=600)
    assumptions = serializers.CharField(max_length=600)
    disaggregation = serializers.IntegerField(required=False)
    entries = serializers.ListField(child=serializers.IntegerField())
    charts = serializers.ListField(child=serializers.IntegerField())
    analysisId = serializers.IntegerField(required=True)

