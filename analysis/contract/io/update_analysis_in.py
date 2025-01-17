"""Request object to create an analysis contract"""
from rest_framework import serializers

from analysis.contract.io.create_analysis_in import DisaggregationSerializer, SectorSerializer


class AnalysisQuestionSerializer(serializers.Serializer):
    """Request input for an AnalysisQuestion creation"""
    id = serializers.IntegerField()
    content = serializers.CharField()


class AnalysisFrameworkSerializer(serializers.Serializer):
    """Request input for an analysis creation"""
    id = serializers.IntegerField()
    name = serializers.CharField()


class UpdateAnalysisIn(serializers.Serializer):
    """Request input for an analysis creation"""
    title = serializers.CharField(max_length=255)
    disaggregations = serializers.ListField(
        child=DisaggregationSerializer(),
        allow_empty=True,
        required=False
    )
    sectors = serializers.ListField(
        child=SectorSerializer(),
        required=False,
        allow_empty=True
    )
    objectives = serializers.CharField(max_length=1000)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    analysis_framework = AnalysisFrameworkSerializer(required=False)
    analysis_questions = serializers.ListField(
        child=AnalysisQuestionSerializer(required=False),
        required=False,
        allow_empty=True
    )
