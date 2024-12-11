"""Request object to create an analysis contract"""
from rest_framework import serializers


class CreateAnalysisIn(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    disaggregations = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    sectors = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    objectives = serializers.CharField(max_length=1000)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    workspace_id = serializers.CharField()
