"""Contains the save chart input"""

from rest_framework import serializers


class SaveChartRequest(serializers.Serializer):
    """The request structure"""

    name = serializers.CharField(max_length=255)
    subpillar_id = serializers.IntegerField()
    x_col = serializers.CharField()
    type = serializers.ChoiceField(choices=["pie", "bar", "line"])
    y_cols = serializers.ListField(child=serializers.CharField())
    title = serializers.CharField(
        max_length=255, allow_null=True, allow_blank=True, required=False
    )
    x_label = serializers.CharField(
        max_length=255, allow_null=True, allow_blank=True, required=False
    )
    y_label = serializers.CharField(
        max_length=255, allow_null=True, allow_blank=True, required=False
    )
    dataset_id = serializers.UUIDField()
    analysis_id = serializers.IntegerField()
