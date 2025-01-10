"""Contains the serializer for updating dataset rows"""

from rest_framework import serializers


class DynamicRowsField(serializers.DictField):
    """Custom field to handle dynamic keys where each value is a list of strings"""

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("This field must be a dictionary")
        for key, value in data.items():
            if not isinstance(value, list) or not all(
                isinstance(item, (str, int, float)) for item in value
            ):
                raise serializers.ValidationError(
                    f"All values for key '{key}' must be a list of strings"
                )
        return super().to_internal_value(data)


class UpdateRowsIn(serializers.Serializer):
    """Serialize the updating rows endpoint's body"""

    page_number = serializers.IntegerField()
    page_size = serializers.IntegerField()
    rows = DynamicRowsField()
    analysis_id = serializers.IntegerField()
