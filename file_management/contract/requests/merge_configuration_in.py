"""Request interface for merging datasets"""
from rest_framework import serializers

class DatasetJoinColumn(serializers.Serializer):
    """A serializer that contains the dataset id and the join column"""
    id = serializers.UUIDField()
    join_column = serializers.CharField(max_length=255, allow_blank=False)


class MergeConfigurationIn(serializers.Serializer):
    """Request interface for merging datasets"""
    datasets = serializers.ListField(child=DatasetJoinColumn(), min_length=2)
    analysis_id = serializers.IntegerField()
    output_name = serializers.CharField(max_length=255, allow_blank=False)
    method = serializers.ChoiceField(choices=[
        "left", "right", "inner", "outer"\
    ], default="left", allow_null=True)
