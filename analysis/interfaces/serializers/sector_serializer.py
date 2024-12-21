"""This module contains the sector serializer"""
from rest_framework import serializers

from analysis.models.sector import Sector

class SectorSerializer(serializers.ModelSerializer):
    """
    Serializer to transform Analysis model to AnalysisTO format.
    """
    id = serializers.CharField(max_length=36, read_only=True)

    class Meta:
        """Base class"""
        model = Sector
        fields = ['id']
