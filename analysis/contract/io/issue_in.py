"""This module contains the sector serializer"""
from rest_framework import serializers


class IssueIn(serializers.ModelSerializer):
    """
    Serializer to transform Issue JSON to Dict format.
    """
    name: str
    description: str
    informationGaps: str
    assumptions: str
    disaggregation: serializers.IntegerField(required=False)
    entries: serializers.ListField(child=serializers.IntegerField())
    charts: serializers.ListField(child=serializers.IntegerField())
    analysisId: serializers.IntegerField(required=True)
