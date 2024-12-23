"""Request object to create an analysis contract"""
from rest_framework import serializers


class UpdateStepsIn(serializers.Serializer):
    """Request input for updating the analysis steps"""
    step_ids = serializers.ListField(
        child=serializers.IntegerField()
    )
