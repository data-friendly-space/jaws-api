"""Request object to update dataset columns"""
from rest_framework import serializers

class ColumnIn(serializers.Serializer):
    """The format of the columns"""
    id = serializers.IntegerField()
    alias = serializers.CharField(allow_null=True)
    data_type_id = serializers.IntegerField(allow_null=True)
    data_role_id = serializers.IntegerField(allow_null=True)
    include = serializers.BooleanField()
    subpillar_id = serializers.IntegerField(allow_null=True)
