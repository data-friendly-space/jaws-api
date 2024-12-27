"""Request object to create an analysis contract"""
from rest_framework import serializers


class AttachFileToAnalysisIn(serializers.Serializer):
    """Request input for an analysis creation"""
    url = serializers.CharField()
    analysis_id = serializers.IntegerField()
