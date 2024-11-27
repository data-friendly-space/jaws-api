from rest_framework import serializers

from analysis.models.disaggregation import Disaggregation


class DisaggregationSerializer(serializers.ModelSerializer):
    """
    Serializer to transform Analysis model to AnalysisTO format.
    """
    id = serializers.CharField(max_length=36, read_only=True)

    class Meta:
        model = Disaggregation
        fields = ['id']