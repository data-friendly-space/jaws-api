"""Request object to create an analysis contract"""
from rest_framework import serializers


class DisaggregationSerializer(serializers.Serializer):
    """Request input for a Disaggregation creation"""
    id = serializers.IntegerField()
    name = serializers.CharField()


class SectorSerializer(serializers.Serializer):
    """Request input for a Sector creation"""
    id = serializers.IntegerField()
    name = serializers.CharField()


class CreateAnalysisIn(serializers.Serializer):
    """Request input for an analysis creation"""
    title = serializers.CharField(max_length=255)
    disaggregations = serializers.ListField(
        child=DisaggregationSerializer(),
        allow_empty=True,
        required=False
    )
    sectors = serializers.ListField(
        child=SectorSerializer()
    )
    objectives = serializers.CharField(max_length=1000)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    workspace_id = serializers.CharField()
