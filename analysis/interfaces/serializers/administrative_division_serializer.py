'''This module contains the disaggregation serializer'''
from rest_framework import serializers

from analysis.models.administrative_division import AdministrativeDivision


class AdministrativeDivisionSerializer(serializers.ModelSerializer):
    """
    Serializer to transform Analysis model to AnalysisTO format.
    """
    p_code = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        '''Base class'''
        model = AdministrativeDivision
        fields = ['p_code', 'name']
