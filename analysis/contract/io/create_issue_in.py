"""This module contains the entry serializer"""
from rest_framework import serializers

from analysis.contract.io.create_entry_in import CreateEntryIn


class CreateIssueIn(serializers.Serializer):
    """
    Serializer to transform Issue JSON to Dict format.
    """
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=600)
    description = serializers.CharField(max_length=600)
    informationGaps = serializers.CharField(max_length=600)
    assumptions = serializers.CharField(max_length=600)
    disaggregation = serializers.IntegerField(required=False)
    entries = serializers.ListField(child=CreateEntryIn())
    charts = serializers.ListField(child=serializers.IntegerField())
    analysisId = serializers.IntegerField(required=True)
